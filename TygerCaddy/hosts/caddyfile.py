import os
import subprocess
from django.conf import settings
from django.contrib.auth.models import User
from dns.models import EVariables

from .models import Host
from config.models import Config
from proxies.models import Header

def generate_caddyfile():
    user = User.objects.get(pk=1)

    project = settings.BASE_DIR
    caddyfilepath = project + '/data/caddyfile.conf'
    caddyfile = open(caddyfilepath, "w+")

    config = Config.objects.get(pk=1)
    if config.dns_provider:
        dns = config.dns_provider
        caddyname = dns.caddy_name
        set_evariables(config=config, dns=dns)

    hosts = Host.objects.all()

    for caddyhost in hosts:
        headerlist = Header.objects.filter(proxy__id=caddyhost.proxy.id)


        block = caddyhost.host_name + ' { \n'
        block += '\t root ' + caddyhost.root_path + '\n'
        block += '\t\t proxy ' + caddyhost.proxy.proxy_from + ' ' + caddyhost.proxy.proxy_to + ' { \n'
        print(caddyhost.proxy)
        if caddyhost.proxy.load_policy:
            block += '\t\t\t load_policy ' + str(caddyhost.proxy.load_policy.name) + '\n'
        if caddyhost.proxy.fail_timeout:
            block += '\t\t\t fail_timeout ' + str(caddyhost.proxy.fail_timeout) + '\n'
        if caddyhost.proxy.max_fails:
            block += '\t\t\t max_fails ' + str(caddyhost.proxy.max_fails) + '\n'
        if caddyhost.proxy.max_conns:
            block += '\t\t\t max_conns ' + str(caddyhost.proxy.max_conns) + '\n'
        if caddyhost.proxy.try_duration:
            block += '\t\t\t try_duration ' + str(caddyhost.proxy.try_duration) + '\n'
        if caddyhost.proxy.try_interval:
            block += '\t\t\t try_interval ' + str(caddyhost.proxy.try_interval) + '\n'
        if caddyhost.proxy.health_check:
            block += '\t\t\t health_check ' + str(caddyhost.proxy.health_check) + '\n'
        if caddyhost.proxy.health_check_port:
            block += '\t\t\t health_check_port ' + str(caddyhost.proxy.health_check_port) + '\n'
        if caddyhost.proxy.health_check_interval:
            block += '\t\t\t health_check_interval ' + str(caddyhost.proxy.health_check_interval) + '\n'
        if caddyhost.proxy.health_check_timeout:
            block += '\t\t\t health_check_timeout ' + str(caddyhost.proxy.health_check_timeout) + '\n'
        if caddyhost.proxy.keep_alive:
            block += '\t\t\t keep_alive ' + str(caddyhost.proxy.keep_alive) + '\n'
        if caddyhost.proxy.timeout:
            block += '\t\t\t timeout ' + str(caddyhost.proxy.timeout) + '\n'
        if caddyhost.proxy.without:
            block += '\t\t\t without ' + str(caddyhost.proxy.without) + '\n'
        if caddyhost.proxy.exceptions:
            block += '\t\t\t exceptions ' + str(caddyhost.proxy.exceptions) + '\n'
        if caddyhost.proxy.insecure_skip_verify:
            block += '\t\t\t insecure_skip_verify \n'
        if caddyhost.proxy.websocket:
            block += '\t\t\t websocket \n'
        if caddyhost.proxy.transparent:
            block += '\t\t\t transparent \n'

        if headerlist:
            for header in headerlist:
                if header.downstream:
                    block += 'header_downstream ' + header.header + ' ' + header.value + '\n'
                if header.upstream:
                    block += 'header_upstream ' + header.header + ' ' + header.value + '\n'

        block += '\t\t } \n'

        if caddyhost.tls == False:
            block += '\ttls off \n } \n \n'
        elif config.dns_challenge:
            block += '\ttls ' + caddyname + '\n } \n \n'
        else:
            block += '\ttls ' + user.email + '\n } \n \n'

    caddyfile.write(block)

    caddyfile.close()
    generate_dash()

    return True

def generate_dash():
    project = settings.BASE_DIR
    caddyfilepath = project + '/data/caddyfile.conf'
    config = Config.objects.get(pk=1)

    block = config.interface + ':' + str(config.port) + ' { \n \n' \
                                                        'proxy / ' + config.proxy_host + ' { \n' \
                                                        'transparent \n' \
                                                        'except ' + config.proxy_exception + '\n' \
                                                        '} \n \n' \
                                                        'root ' + str(config.root_dir) + '\n' \
                                                        '} \n'

    caddyfile = open(caddyfilepath, "a+")
    caddyfile.write(block)
    caddyfile.close()

    return True


def set_evariables(config, dns):
    variables = EVariables.objects.filter(dns_provider_id=dns.id)

    for var in variables:
        os.environ[var.variable] = str(var.value)
        print(os.environ[var.variable])



