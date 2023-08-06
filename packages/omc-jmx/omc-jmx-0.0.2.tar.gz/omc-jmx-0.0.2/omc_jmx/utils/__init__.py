import pkg_resources

class JmxTermUtils:
    @staticmethod
    def build_command(command):
        jmxterm = pkg_resources.resource_filename('omc_jmx.lib', 'jmxterm-1.0.2-uber.jar')
        jmx_cmd = 'echo "%s"  | java -jar %s -n' % (command, jmxterm)
        return jmx_cmd

    @staticmethod
    def get_resource():
        jmxterm = pkg_resources.resource_filename('omc_jmx.lib', 'jmxterm-1.0.2-uber.jar')
        return jmxterm

