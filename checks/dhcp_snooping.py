def dhcp_check(iface_params, vlanmap, allinterf, enabled,result_dict,scale):
    if (enabled):
        try:
            iface_snoop = iface_params['dhcp_snoop']
        except:
            pass
        iface_vlans = []
        # check if interface has vlans on it
        if 'vlans' in iface_params:
            iface_vlans = iface_params['vlans']
        # check if interface is turned off, and if we need to check disabled interfaces
        if (not (allinterf) and iface_params['shutdown'] == 'yes'):
            pass
        else:
            # create dictionary for output
            if not ('DHCP snooping' in result_dict):
                result_dict['DHCP snooping'] = {}
            mode = iface_snoop['mode']
        if (mode == 'untrust'):
            # check if limit is set and range is good
            if 'limit' in iface_snoop:
                chkres = 0
                chkres = int(iface_snoop['limit'][0]) > 100
                # need to handle something like '100 burst 10'
                # except:
                #     print(int(iface_snoop['limit'][0].split(' ')[0]))
                #     # push first number
                #     chkres = int(iface_snoop['limit'][0].split(' ')[0]) > 100
                if (chkres):
                    result_dict['DHCP snooping']['rate limit'] = [scale[1], 'Too high','DHCP starvation prevention is inefficient']
                else:
                    result_dict['DHCP snooping']['rate limit'] = [scale[2], 'OK','DHCP starvation prevention is efficient']

            else:
                result_dict['DHCP snooping']['rate limit'] = [scale[1], 'Not set', 'Needed to prevent DHCP starvation']
        # check if trusted interface is marked as trusted in vlamap
        elif ((mode == 'trust') and vlanmap and iface_vlans):
            if (set(vlanmap[2]).isdisjoint(iface_vlans)):
                result_dict['DHCP snooping']['vlans'] = [scale[0], 'Interface set as trusted, but vlanmap is different',
                                                         'This interface is not trusted according to vlanmap, but marked as trusted. Unauthorized DHCP server can work here']
        else:
            result_dict = 0
    return result_dict

def check(iface_params, vlanmap, allinterf, enabled, vlanmap_type):
    result = {}

# If this network segment is TRUSTED - enabled cdp is not a red type of threat, it will be colored in orange
    if vlanmap_type == 'TRUSTED':
        dhcp_check(iface_params, vlanmap, allinterf, enabled,result,[1,1,2])

# Otherwise if network segment is CRITICAL or UNKNOWN or vlanmap is not defined - enabled cdp is a red type of threat
    else:
        dhcp_check(iface_params, vlanmap, allinterf, enabled,result, [0,1, 2])

    return result

