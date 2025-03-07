import streamlit as st
import xml.etree.ElementTree as ET
import xml.dom.minidom

if "mapped_folders" not in st.session_state:
    st.session_state.mapped_folders = []

st.title("Windows Sandbox Configuration Generator")

st.html("<hr></hr>")

st.subheader("vGPU", help="Enables or Disables the Sandbox Virtual GPU")
vgpu = st.selectbox("Enable vGPU?", ["Enable", "Disable"])

st.subheader("Networking", help="Enables or Disables the Sandbox inbuilt network Network, Used Hyper-V default Switch")
networking = st.selectbox("Enable Networking?", ["Enable", "Disable"])

st.subheader("Mapped Folder Configuration", help="Adds mapped folders from the Host Machine to the Sandbox. If folders are added sources and destinations **MUST** be supplied")
if st.button("Add Mapped Folder"):
    st.session_state.mapped_folders.append({"host": "", "sandbox": "C:\\Users\\WDAGUtilityAccount\\", "read_only": False})
for folder_id, folder in enumerate(st.session_state.mapped_folders):
    st.text_input(f"Host Folder Path", folder["host"], key=f"host_{folder_id}")
    st.text_input(f"Sandbox Folder Path", folder["sandbox"], key=f"sandbox_{folder_id}", help="WDAGUtilityAccount is the default account on the Sandbox")
    st.checkbox(f"Read-Only?", folder["read_only"], key=f"readonly_{folder_id}")
    if st.button("Delete Mapped Folders"):  
        del st.session_state.mapped_folders[folder_id]


st.subheader("Logon Command", help="Defines Command to run at Sandbox logon, field does not have to be filled if you have no command to run")
logon_command_in = st.text_input("Logon Command", "")

st.subheader("Audio Input", help="Enables or Disables the Audio Input for the Sandbox (Microphone)")
audio_input_in = st.selectbox("Enable Audio Input", ["Enable", "Disable"])

st.subheader("Video Input", help="Enables or Disables the Video Input for the Sandbox (Camera)")
video_input_in = st.selectbox("Enable Video Input", ["Enable", "Disable"])

st.subheader("Protected Client", help="Enables or Disables Protected Client, Runs applications inside AppContainer Isolation execution environment. Visit https://learn.microsoft.com/en-us/windows/win32/secauthz/appcontainer-isolation")
protected_client = st.selectbox("Enable Protected Client?", ["Enable", "Disable"])

st.subheader("Printer Redirection", help="Enables or Disables Printer Redirection, allows host to share printers with Sandbox")
printer_redirection = st.selectbox("Enable Printer Redirection?", ["Enable", "Disable"])

st.subheader("Clipboard Redirection", help="Enables or Disables Clipboard Redirection, allows host to share clipboard with Sandbox, and vice versa")
clipboard_redirection = st.selectbox("Enable Clipbpard Redirection?", ["Enable", "Disable"])

st.subheader("Memory in MiB", help="Defines the amount of memory available to the Sandbox, anything under 2048 will be ignored")
memory_in_mib_in = st.text_input("Memory in MiB")

st.html("<hr></hr>")
st.subheader("Presets")

col1, col2, col3 = st.columns(3)

with col1:
    if st.button("Default"):
        vgpu = "Enable"
        networking = "Enable"
        audio_input_in = "Enable"
        video_input_in = "Enable"
        protected_client = "Enable"
        printer_redirection = "Enable"
        clipboard_redirection = "Enable"

with col2:
    if st.button("Locked Down"):
        vgpu = "Disable"
        networking = "Disable"
        audio_input_in = "Disable"
        video_input_in = "Disable"
        protected_client = "Enable"
        printer_redirection = "Disable"
        clipboard_redirection = "Disable"

with col3:
    if st.button("Lockdown + Net"):
        vgpu = "Disable"
        networking = "Enable"
        audio_input_in = "Disable"
        video_input_in = "Disable"
        protected_client = "Enable"
        printer_redirection = "Disable"
        clipboard_redirection = "Disable"

st.html("<hr></hr>") 

# XML Nightmare
configuration = ET.Element("Configuration")
ET.SubElement(configuration, "VGpu").text = vgpu 
ET.SubElement(configuration, "Networking").text = networking 

if st.session_state.mapped_folders:
    mapped_folders = ET.SubElement(configuration, "MappedFolders")
    for folder_id, folder in enumerate(st.session_state.mapped_folders):
        mapped_folder = ET.SubElement(mapped_folders, "MappedFolder")
        ET.SubElement(mapped_folder, "HostFolder").text = st.session_state[f"host_{folder_id}"]
        ET.SubElement(mapped_folder, "SandboxFolder").text = st.session_state[f"sandbox_{folder_id}"]
        ET.SubElement(mapped_folder, "ReadOnly").text = str(st.session_state[f"readonly_{folder_id}"]).lower()

logon_command = ET.SubElement(configuration, "LogonCommand")
ET.SubElement(logon_command, "Command").text = logon_command_in
ET.SubElement(configuration, "AudioInput").text = audio_input_in
ET.SubElement(configuration, "VideoInput").text = video_input_in
ET.SubElement(configuration, "ProtectedClient").text = protected_client
ET.SubElement(configuration, "PrinterRedirection").text = printer_redirection
ET.SubElement(configuration, "ClipboardRedirection").text = clipboard_redirection
ET.SubElement(configuration,"MemoryInMB").text = memory_in_mib_in

xml_string = '<?xml version="1.0" encoding="UTF-8"?>\n' + ET.tostring(configuration, encoding="unicode")
xml_pretty = xml.dom.minidom.parseString(xml_string).toprettyxml(indent="  ")

st.subheader("Generated XML:")
st.code(xml_pretty, language="xml")

st.download_button(
    label="Download WSB File",
    data=xml_pretty,
    file_name="sandbox_configuration.wsb",
    mime="application/xml"
)

st.html("<hr></hr>")
st.write("Read up more on Windows Sandbox here!")
st.write("https://learn.microsoft.com/en-us/windows/security/application-security/application-isolation/windows-sandbox/")
st.html("<a href='https://github.com/BiscottiMuncher'>Evan Metzinger 2025</a>")
