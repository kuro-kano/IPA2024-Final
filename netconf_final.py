from ncclient import manager
import xmltodict

# Connect to device (adjust host/port if needed)
m = manager.connect(
    host="10.0.15.61",
    port=830,
    username="admin",
    password="cisco",
    hostkey_verify=False,
)

def netconf_edit_config(netconf_config):
    return m.edit_config(target="running", config=netconf_config)


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


def create():
    netconf_config = """
    <config>
      <interfaces xmlns="urn:ietf:params:xml:ns:yang:ietf-interfaces">
        <interface>
          <name>Loopback66070091</name>
          <type xmlns:ianaift="urn:ietf:params:xml:ns:yang:iana-if-type">ianaift:softwareLoopback</type>
          <enabled>true</enabled>
          <ietf-ip:ipv4 xmlns:ietf-ip="urn:ietf:params:xml:ns:yang:ietf-ip">
            <address>
              <ip>172.0.91.1</ip>
              <netmask>255.255.255.0</netmask>
            </address>
          </ietf-ip:ipv4>
        </interface>
      </interfaces>
    </config>
    """

    try:
        reply = netconf_edit_config(netconf_config)
        xml_data = reply.xml
        print(xml_data)
        if "<ok/>" in xml_data:
            return "Interface Loopback66070091 is created successfully"
        else:
            return "Error: Cannot create Interface Loopback66070091"
    except Exception as e:
        print(f"Exception: {e}")
        return f"Error: Cannot connect to router - {str(e)}"


def delete():
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
        reply = netconf_edit_config(netconf_config)
        xml_data = reply.xml
        print(xml_data)
        if "<ok/>" in xml_data:
            return "Interface Loopback66070091 is deleted successfully"
        else:
            return "Cannot delete: Interface Loopback66070091"
    except Exception as e:
        print(f"Exception: {e}")
        return f"Error: Cannot connect to router - {str(e)}"


def enable():
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
        reply = netconf_edit_config(netconf_config)
        xml_data = reply.xml
        print(xml_data)
        if "<ok/>" in xml_data:
            return "Interface Loopback66070091 is enabled successfully"
        else:
            return "Cannot enable: Interface Loopback66070091"
    except Exception as e:
        print(f"Exception: {e}")
        return f"Error: Cannot connect to router - {str(e)}"


def disable():
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
        reply = netconf_edit_config(netconf_config)
        xml_data = reply.xml
        print(xml_data)
        if "<ok/>" in xml_data:
            return "Interface Loopback66070091 is disabled successfully"
        else:
            return "Cannot disable: Interface Loopback66070091"
    except Exception as e:
        print(f"Exception: {e}")
        return f"Error: Cannot connect to router - {str(e)}"


def status():
    netconf_filter = """
    <interfaces-state xmlns="urn:ietf:params:xml:ns:yang:ietf-interfaces">
      <interface>
        <name>Loopback66070091</name>
      </interface>
    </interfaces-state>
    """

    try:
        netconf_reply = m.get(filter=("subtree", netconf_filter))
        print(netconf_reply)
        netconf_reply_dict = xmltodict.parse(netconf_reply.xml)

        interfaces_state = _find_key(netconf_reply_dict, "interfaces-state")
        if interfaces_state:
            interface = interfaces_state.get("interface")
            # interface may be a list or dict
            if isinstance(interface, list):
                interface = interface[0]
            admin_status = _find_key(interface, "admin-status")
            oper_status = _find_key(interface, "oper-status")
            # xmltodict may return values as dicts with '#text'
            if isinstance(admin_status, dict):
                admin_status = admin_status.get("#text", "")
            if isinstance(oper_status, dict):
                oper_status = oper_status.get("#text", "")

            if admin_status == "up" and oper_status == "up":
                return "Interface Loopback66070091, Status: Enabled"
            elif admin_status == "down" and oper_status == "down":
                return "Interface Loopback66070091, Status: Disabled"
            else:
                return f"Interface Loopback66070091, Admin: {admin_status}, Oper: {oper_status}"
        else:
            return "Error: No Interface Loopback66070091"
    except Exception as e:
        print(f"Exception: {e}")
        return f"Error: Cannot connect to router - {str(e)}"
