from ncclient import manager
import xmltodict


def get_manager(host, port=830, username="admin", password="cisco"):
    return manager.connect(
        host=host,
        port=port,
        username=username,
        password=password,
        hostkey_verify=False,
    )


def netconf_edit_config(mgr, netconf_config):
    return mgr.edit_config(target="running", config=netconf_config)


def _find_key(data, suffix):
    if isinstance(data, dict):
        for k, v in data.items():
            if k.endswith(suffix):
                return v
            res = _find_key(v, suffix)
            if res is not None:
                return res
    elif isinstance(data, list):
        for item in data:
            res = _find_key(item, suffix)
            if res is not None:
                return res
    return None


def create(device_ip):
    netconf_config = """
    <config>
      <interfaces xmlns="urn:ietf:params:xml:ns:yang:ietf-interfaces">
        <interface>
          <name>Loopback66070091</name>
          <type xmlns:ianaift="urn:ietf:params:xml:ns:yang:iana-if-type">ianaift:softwareLoopback</type>
          <enabled>true</enabled>
          <ietf-ip:ipv4 xmlns:ietf-ip="urn:ietf:params:xml:ns:yang:ietf-ip">
            <ietf-ip:address>
              <ietf-ip:ip>172.0.91.1</ietf-ip:ip>
              <ietf-ip:netmask>255.255.255.0</ietf-ip:netmask>
            </ietf-ip:address>
          </ietf-ip:ipv4>
        </interface>
      </interfaces>
    </config>
    """

    try:
        with get_manager(device_ip) as m:
            reply = netconf_edit_config(m, netconf_config)
            xml_data = reply.xml
            print(xml_data)
            if "<ok/>" in xml_data:
                return "Interface Loopback66070091 is created successfully using NETCONF"
            else:
                return "Error: Cannot create Interface Loopback66070091 (checked via NETCONF)"
    except Exception as e:
        print(f"Exception: {e}")
        return f"Error: Cannot connect to router {device_ip} - {str(e)}"


def delete(device_ip):
    netconf_config = """
    <config xmlns:nc="urn:ietf:params:xml:ns:netconf:base:1.0">
      <interfaces xmlns="urn:ietf:params:xml:ns:yang:ietf-interfaces">
        <interface nc:operation="delete">
          <name>Loopback66070091</name>
        </interface>
      </interfaces>
    </config>
    """

    try:
        with get_manager(device_ip) as m:
            reply = netconf_edit_config(m, netconf_config)
            xml_data = reply.xml
            print(xml_data)
            if "<ok/>" in xml_data:
                return "Interface Loopback66070091 is deleted successfully using NETCONF"
            else:
                return "Cannot delete: Interface Loopback66070091 (checked via NETCONF)"
    except Exception as e:
        print(f"Exception: {e}")
        return f"Error: Cannot connect to router {device_ip} - {str(e)}"


def enable(device_ip):
    netconf_config = """
    <config>
      <interfaces xmlns="urn:ietf:params:xml:ns:yang:ietf-interfaces">
        <interface>
          <name>Loopback66070091</name>
          <enabled>true</enabled>
        </interface>
      </interfaces>
    </config>
    """

    try:
        with get_manager(device_ip) as m:
            reply = netconf_edit_config(m, netconf_config)
            xml_data = reply.xml
            print(xml_data)
            if "<ok/>" in xml_data:
                return "Interface Loopback66070091 is enabled successfully using NETCONF"
            else:
                return "Cannot enable: Interface Loopback66070091 (checked via NETCONF)"
    except Exception as e:
        print(f"Exception: {e}")
        return f"Error: Cannot connect to router {device_ip} - {str(e)}"


def disable(device_ip):
    netconf_config = """
    <config>
      <interfaces xmlns="urn:ietf:params:xml:ns:yang:ietf-interfaces">
        <interface>
          <name>Loopback66070091</name>
          <enabled>false</enabled>
        </interface>
      </interfaces>
    </config>
    """

    try:
        with get_manager(device_ip) as m:
            reply = netconf_edit_config(m, netconf_config)
            xml_data = reply.xml
            print(xml_data)
            if "<ok/>" in xml_data:
                return "Interface Loopback66070091 is disabled successfully using NETCONF"
            else:
                return "Cannot disable: Interface Loopback66070091 (checked via NETCONF)"
    except Exception as e:
        print(f"Exception: {e}")
        return f"Error: Cannot connect to router {device_ip} - {str(e)}"


def status(device_ip):
    netconf_filter = """
    <interfaces-state xmlns="urn:ietf:params:xml:ns:yang:ietf-interfaces">
      <interface>
        <name>Loopback66070091</name>
      </interface>
    </interfaces-state>
    """

    try:
        with get_manager(device_ip) as m:
            netconf_reply = m.get(filter=("subtree", netconf_filter))
            print(netconf_reply)
            netconf_reply_dict = xmltodict.parse(netconf_reply.xml)

            interfaces_state = _find_key(netconf_reply_dict, "interfaces-state")
            if interfaces_state:
                interface = interfaces_state.get("interface")
                if isinstance(interface, list):
                    interface = interface[0]
                admin_status = _find_key(interface, "admin-status")
                oper_status = _find_key(interface, "oper-status")
                if isinstance(admin_status, dict):
                    admin_status = admin_status.get("#text", "")
                if isinstance(oper_status, dict):
                    oper_status = oper_status.get("#text", "")

                if admin_status == "up" and oper_status == "up":
                    return "Interface Loopback66070091, Status: Enabled (checked via NETCONF)"
                elif admin_status == "down" and oper_status == "down":
                    return "Interface Loopback66070091, Status: Disabled (checked via NETCONF)"
                else:
                    return f"Interface Loopback66070091, Admin: {admin_status}, Oper: {oper_status} (checked via NETCONF)"
            else:
                return "Error: No Interface Loopback66070091 (checked via NETCONF)"

    except Exception as e:
        print(f"Exception: {e}")
        return f"Error: Cannot connect to router {device_ip} - {str(e)}"
