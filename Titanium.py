import sublime_plugin
import json
import subprocess


class TitaniumCommand(sublime_plugin.WindowCommand):

    def run(self, *args, **kwargs):
        self.platforms = ["android", "ios", "mobileweb"]
        self.window.show_quick_panel(self.platforms, self.select_platform)

    def select_platform(self, select):
        if (select < 0):
            return
        self.platform = self.platforms[select]
        if self.platform == "ios":
            self.targets = ["simulator", "device"]
            self.window.show_quick_panel(self.targets, self.select_ios_target)
        elif self.platform == "android":
            self.targets = ["emulator", "device", "dist-appstore", "dist-adhoc"]
            self.window.show_quick_panel(self.targets, self.select_android_target)
        else:
            self.run_titanium()  # mobile web

    def load_android_avds(self):
        process = subprocess.Popen(["android", "list", "avd", "-c"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        result, error = process.communicate()
        self.avds = result.split()

    def select_android_target(self, select):
        if (select < 0):
            return
        target = self.targets[select]
        if (target == "emulator"):
            self.load_android_avds()
            self.window.show_quick_panel(self.avds, self.select_android_avd)
        else:
            self.run_titanium(["--target", target])

    def select_android_avd(self, select):
        if (select < 0):
            return
        self.run_titanium(["--avd-id", self.avds[select]])

    def select_ios_target(self, select):
        if (select < 0):
            return
        target = self.targets[select]
        if (target == "device"):
            self.load_ios_info()
            self.target = 'development'
            self.window.show_quick_panel(self.certs[self.target], self.select_ios_cert)
        else:
            self.run_titanium()  # run simulator

    def select_ios_cert(self, select):
        if (select < 0):
            return
        self.cert = self.certs[self.target][select]
        self.window.show_quick_panel(self.profiles[self.target], self.select_ios_profile)

    def select_ios_profile(self, select):
        if (select < 0):
            return
        name, profile = self.profiles[self.target][select]
        self.run_titanium(["--target", "device", "--pp-uuid", profile, "--developer-name", self.cert])

    def load_ios_info(self):
        process = subprocess.Popen(["titanium", "info", "--types", "ios", "--output", "json"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        result, error = process.communicate()
        info = json.loads(result)
        self.certs = {}
        self.profiles = {}
        for name, obj in info.items():
            if name == "iosCerts":
                for target, c in obj.items():
                    if target == "devNames":
                        target = "development"
                    elif target == "distNames":
                        target = "distribution"
                    else:
                        continue
                    l = []
                    for cert in c:
                        l.append(cert)
                    self.certs[target] = l
            elif name == "iOSProvisioningProfiles":
                for target, p in obj.items():
                    l = []
                    for profile in p:
                        l.append([profile['name'], profile['uuid']])
                    self.profiles[target] = l

    def run_titanium(self, options=[]):
        folder = self.window.folders()[0]
        cmd = ["titanium", "build", "--project-dir", folder, "--no-colors", "--platform", self.platform]
        cmd.extend(options)
        self.window.run_command("exec", {"cmd": cmd})
