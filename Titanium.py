import sublime
import sublime_plugin
import json
import subprocess
from os.path import expanduser

class TitaniumCommand(sublime_plugin.WindowCommand):

    def run(self, *args, **kwargs):
        settings = sublime.load_settings('Titanium.sublime-settings')
        self.cli              = settings.get("titaniumCLI", "/usr/bin/titanium")
        self.android          = settings.get("androidSDK", "/opt/android-sdk") + "/tools/android"
        self.loggingLevel     = settings.get("loggingLevel", "info")
        self.simulatorType    = settings.get("simulatorType", False)
        self.simulatorRetina  = settings.get("simulatorRetina", False)
        self.simulatorTall    = settings.get("simulatorTall", False)
        self.iosVersion       = settings.get("iosVersion", False)
        self.iosSimVersion    = settings.get("iosSimVersion", False)
        self.genymotionCLI    = str(settings.get("genymotionCLI", "/Applications/Genymotion Shell.app/Contents/MacOS/genyshell"))

        folders = self.window.folders()
        if len(folders) <= 0:
            self.show_quick_panel(["ERROR: Must have a project open"], None)
        else:
            if len(folders) == 1:
                self.multipleFolders = False
                self.project_folder = folders[0]
                self.project_sdk = self.get_project_sdk_version()
                self.pick_platform()
            else:
                self.multipleFolders = True
                self.pick_project_folder(folders)

    def pick_project_folder(self, folders):
        folderNames = []
        for folder in folders:
            index = folder.rfind('/') + 1
            if index > 0:
                folderNames.append(folder[index:])
            else:
                folderNames.append(folder)

        # only show most recent when there is a command stored
        if 'titaniumMostRecent' in globals():
            folderNames.insert(0, 'most recent configuration')

        self.show_quick_panel(folderNames, self.select_project)

    def select_project(self, select):
        folders = self.window.folders()
        if select < 0:
            return

        # if most recent was an option, we need subtract 1
        # from the selected index to match the folders array
        # since the "most recent" option was inserted at the beginning
        if 'titaniumMostRecent' in globals():
            select = select - 1

        if select == -1:
            self.window.run_command("exec", {"cmd": titaniumMostRecent})
        else:
            self.project_folder = folders[select]
            self.project_sdk = self.get_project_sdk_version()
            self.pick_platform()


    def pick_platform(self):
        self.platforms = ["android", "ios", "mobileweb", "clean"]

        # only show most recent when there are NOT multiple top level folders
        # and there is a command stored
        if self.multipleFolders == False and 'titaniumMostRecent' in globals():
            self.platforms.insert(0, 'most recent configuration')

        self.show_quick_panel(self.platforms, self.select_platform)

    def select_platform(self, select):
        if select < 0:
            return
        self.platform = self.platforms[select]

        if self.platform == "most recent configuration":
            self.window.run_command("exec", {"cmd": titaniumMostRecent})
        elif self.platform == "ios":
            self.targets = ["simulator", "device", "dist-appstore", "dist-adhoc"]
            self.show_quick_panel(self.targets, self.select_ios_target)
        elif self.platform == "android":
            self.targets = ["GenyMotion", "emulator", "device", "dist-playstore"]
            self.show_quick_panel(self.targets, self.select_android_target)
        elif self.platform == "mobileweb":
            self.targets = ["development", "production"]
            self.show_quick_panel(self.targets, self.select_mobileweb_target)
        else:  # clean project
            self.window.run_command("exec", {"cmd": [self.cli, "clean", "--no-colors", "--project-dir", self.project_folder]})

    # Sublime Text 3 requires a short timeout between quick panels
    def show_quick_panel(self, options, done):
        sublime.set_timeout(lambda: self.window.show_quick_panel(options, done), 10)

    # get the current project's SDK from tiapp.xml
    def get_project_sdk_version(self):
        process = subprocess.Popen([self.cli, "project", "sdk-version", "--project-dir", self.project_folder, "--output=text"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        result, error = process.communicate()
        return result.decode('utf-8').rstrip('\n')

    def run_titanium(self, options=[]):
        cmd = [self.cli, "build", "--sdk", self.project_sdk, "--project-dir", self.project_folder, "--no-colors", "--platform", self.platform, "--log-level", self.loggingLevel]

        project_sdk = self.project_sdk.split('.')

        if (self.iosVersion is not "unknown" and self.iosVersion is not ""):
            if int(project_sdk[0]) < 3 or int(project_sdk[1]) < 2:
                ios_version = self.iosVersion.split('.')
                options.extend(["--ios-version", ios_version[0] + "." + ios_version[1]])
            else:
                options.extend(["--ios-version", self.iosVersion])

        if (self.iosSimVersion is not "unknown" and self.iosSimVersion is not ""):
            if int(project_sdk[0]) < 3 or int(project_sdk[1]) < 2:
                sim_version = self.iosSimVersion.split('.')
                options.extend(["--sim-version", sim_version[0] + "." + sim_version[1]])
            else:
                options.extend(["--sim-version", self.iosSimVersion])
        cmd.extend(options)

        # save most recent command
        global titaniumMostRecent
        titaniumMostRecent = cmd

        self.window.run_command("exec", {"cmd": cmd})

    def run_genymotion(self, options=[]):
        cmd = [self.cli, "build", "--sdk", self.project_sdk, "--project-dir", self.project_folder, "--no-colors", "--platform", self.platform, "--log-level", self.loggingLevel]
        cmd.extend(options)

        # save most recent command
        global titaniumMostRecent
        titaniumMostRecent = cmd

        self.window.run_command("exec", {"cmd": cmd})

    #--------------------------------------------------------------
    # MOBILE WEB
    #--------------------------------------------------------------

    def select_mobileweb_target(self, select):
        if select < 0:
            return
        self.run_titanium(["--deploy-type", self.targets[select]])

    #--------------------------------------------------------------
    # ANDROID
    #--------------------------------------------------------------

    def load_android_avds(self):
        process = subprocess.Popen([self.android, "list", "avd", "-c"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        result, error = process.communicate()
        self.avds = result.split()

    def load_genymotion_vms(self):
        cmd = '"' + self.genymotionCLI + '" -c "devices list" | grep ^[[:space:]] | grep [0-9] | grep "On" | awk -F\'|\' \'{ip=gsub(/^[ \\t]+|[ \\t]+$/, "", $5); name=gsub(/^[ \\t]+|[ \\t]+$/, "", $6); print $5","$6}\''
        process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
        result, error = process.communicate()

        if result != '' and result != None:
            l = []
            for a in result.splitlines():
                ip = a.split(',')[0]
                name = a.split(',')[1]
                l.append([name, ip])
            self.genymotionvms = l
        else:
            sublime.error_message("No running GenyMotion devices found")

    def select_android_target(self, select):
        if select < 0:
            return
        target = self.targets[select]
        if (target == "emulator"):
            self.load_android_avds()
            self.show_quick_panel(self.avds, self.select_android_avd)
        elif (target == "GenyMotion"):
            self.load_genymotion_vms();
            self.show_quick_panel(self.genymotionvms, self.select_genymotion_vm)
        else:
            self.run_titanium(["--target", target])

    def select_android_avd(self, select):
        if select < 0:
            return
        self.run_titanium(["--avd-id", self.avds[select]])

    def select_genymotion_vm(self, select):
        if select < 0:
            return
        self.genymotionname, self.genymotionip = self.genymotionvms[select]
        self.run_genymotion(["--device-id", self.genymotionname])

    #--------------------------------------------------------------
    # IOS
    #--------------------------------------------------------------

    def select_ios_target(self, select):
        if select < 0:
            return
        self.target = self.targets[select]
        self.load_ios_sdk_info()
        if self.target == "simulator":
            self.prompt_ios_simtype()
        else:
            self.families = ["iphone", "ipad", "universal"]
            self.show_quick_panel(self.families, self.select_ios_family)

    def prompt_ios_simtype(self):
        if not self.simulatorType:
            self.simtype = ["iphone", "iphone-retina", "iphone-retina-tall", "ipad", "ipad-retina", "ipad-retina-tall"]
            self.show_quick_panel(self.simtype, self.select_ios_simtype)
        else:
            self.prompt_ios_sdkversion()

    def select_ios_simtype(self, select):
        if select < 0:
            return
        if (self.simtype[select] == 'iphone'):
            # iphone 4
            self.simulatorType = 'iphone'
            self.simulatorRetina = False
            self.simulatorTall = False
        elif (self.simtype[select] == "iphone-retina"):
            self.simulatorType = 'iphone'
            self.simulatorRetina = True
            self.simulatorTall = False
        elif (self.simtype[select] == "iphone-retina-tall"):
            self.simulatorType = 'iphone'
            self.simulatorRetina = True
            self.simulatorTall = True
        elif (self.simtype[select] == "ipad"):
            self.simulatorType = 'ipad'
            self.simulatorRetina = False
            self.simulatorTall = False
        elif (self.simtype[select] == "ipad-retina"):
            self.simulatorType = 'ipad'
            self.simulatorRetina = True
            self.simulatorTall = False
        elif (self.simtype[select] == "ipad-retina-tall"):
            self.simulatorType = 'ipad'
            self.simulatorRetina = True
            self.simulatorTall = True

        self.prompt_ios_sdkversion()

    def prompt_ios_sdkversion(self):
        if not self.iosVersion:
            sdk_version_list = []
            for sdk_version in self.sdkvers:
                sdk_version_list.append("iOS SDK: " + sdk_version)
            self.show_quick_panel(sdk_version_list, self.select_ios_sdkversion)
        else:
            self.prompt_ios_simversion()

    def select_ios_sdkversion(self, select):
        if select < 0:
            return
        self.iosVersion = self.sdkvers[select]
        self.prompt_ios_simversion()

    def prompt_ios_simversion(self):
        if not self.iosSimVersion:
            sim_version_list = []
            for sim_version in self.simvers:
                sim_version_list.append("iOS Simulator: " + sim_version)
            self.show_quick_panel(sim_version_list, self.select_ios_simversion)
        else: 
            self.run_ios_simulator()

    def select_ios_simversion(self, select):
        if select < 0:
            return
        self.iosSimVersion = self.simvers[select]
        self.run_ios_simulator()

    def run_ios_simulator(self):
        simulatorDisplay = ''
        simulatorHeight = ''
        if self.simulatorRetina:
            simulatorDisplay = '--retina'
        if self.simulatorTall:
            simulatorHeight = '--tall'
        self.run_titanium(["--sim-type", self.simulatorType, simulatorDisplay, simulatorHeight])

    def select_ios_family(self, select):
        if select < 0:
            return
        self.family = self.families[select]
        self.load_ios_info()
        self.show_quick_panel(self.certs, self.select_ios_cert)

    def select_ios_cert(self, select):
        if select < 0:
            return
        self.cert = self.certs[select]
        self.show_quick_panel(self.devices, self.select_ios_device)

    def select_ios_device(self, select):
        if select < 0:
            return
        self.devicename, self.deviceudid = self.devices[select]
        self.show_quick_panel(self.profiles, self.select_ios_profile)

    def select_ios_profile(self, select):
        if select < 0:
            return
        name, profile = self.profiles[select]
        options = ["--target", self.target, "--pp-uuid", profile, "--device-family", self.family]

        if self.target == "device":
            options.extend(["--developer-name", self.cert[0]])
            options.extend(["--device-id", self.deviceudid])
        else:
            options.extend(["--distribution-name", self.cert])

        if self.target == "dist-adhoc":
            options.extend(["--output-dir", self.project_folder + "/dist"])

        self.run_titanium(options)

    def load_ios_sdk_info(self):
        process = subprocess.Popen([self.cli, "info", "--types", "ios", "--output", "json"], stdout = subprocess.PIPE, stderr = subprocess.PIPE)
        result, error = process.communicate()
        info = json.loads(result.decode('utf-8'))

        for name, obj in list(info["xcode"].items()):
            self.sdkvers = sorted(obj["sdks"], reverse = True)
            self.simvers = sorted(obj["sims"], reverse = True)

    def load_ios_info(self):
        process = subprocess.Popen([self.cli, "info", "--types", "ios", "--output", "json"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        result, error = process.communicate()
        info = json.loads(result.decode('utf-8'))

        for name, obj in list(info["ios"].items()):
            if name == "certs":
                for target, c in list(obj["keychains"][expanduser("~") + "/Library/Keychains/login.keychain"].items()):
                    if target == "wwdr" or (target == "developer" and self.target != "device") or (target == "distribution" and self.target == "device"):
                        continue
                    l = []
                    for cert in c:
                        if cert['expired'] is False:
                            l.append([cert['name']])
                    self.certs = l
            elif name == "provisioningProfiles":
                for target, p in list(obj.items()):
                    # TODO: figure out what to do with enterprise profiles
                    if (target == "development" and self.target == "device") or (target == "distribution" and self.target == "dist-appstore") or (target == "adhoc" and self.target == "dist-adhoc"):
                        l = []
                        for profile in p:
                            if profile['expired'] is False:
                                l.append([profile['name'], profile['uuid']])
                        self.profiles = l
            elif name == "devices":
                l = []
                for a in obj:
                    l.append([a['name'], a['udid']])
                self.devices = l
