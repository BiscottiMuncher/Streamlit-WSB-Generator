import streamlit as st
import xml.etree.ElementTree as ET
import xml.dom.minidom


# Create mapped_folders session state
if "mapped_folders" not in st.session_state:
    st.session_state.mapped_folders = []

# Title
st.title("Windows Sandbox Configuration Generator")

st.html("<hr></hr>")


# vGPU switch
st.subheader("vGPU", help="Enabled or Disables the Sandbox Virtual GPU")
vgpu = st.selectbox("Enable vGPU?", ["Enable", "Disable"])

# Networking Switch
st.subheader("Networking", help="Enabled or Disables the Sandbox inbuilt network Network, Used Hyper-V default Switch")
networking = st.selectbox("Enable Networking?", ["Enable", "Disable"])

# Mapped Folder Configuration
st.subheader("Mapped Folder Configuration", help="Adds mapped folders from the Host Machine to the Sandbox. If folders are added sources and destinations **MUST** be supplied")
if st.button("Add Mapped Folder"):
    st.session_state.mapped_folders.append({"host": "", "sandbox": "C:\\Users\\WDAGUtilityAccount\\", "read_only": False})
for idx, folder in enumerate(st.session_state.mapped_folders):
    st.text_input(f"Host Folder Path", folder["host"], key=f"host_{idx}")
    st.text_input(f"Sandbox Folder Path", folder["sandbox"], key=f"sandbox_{idx}", help="WDAGUtilityAccount is the default account on the Sandbox")
    st.checkbox(f"Read-Only?", folder["read_only"], key=f"readonly_{idx}")

# Logon Command Definition
st.subheader("Logon Command", help="Defined Command to run at Sandbox logon, field does not have to be filled if you have no command to run")
logon_command_in = st.text_input("Logon Command", "")

# Audio Input Switch
st.subheader("Audio Input", help="Enables or Disables the Audio Input for the Sandbox (Microphone)")
audio_input_in = st.selectbox("Enable Audio Input", ["Enable", "Disable"])

# Video Input Switch
st.subheader("Video Input", help="Enables or Disables the Video Input for the Sandbox (Camera)")
video_input_in = st.selectbox("Enable Video Input", ["Enable", "Disable"])

# Protected Client Switch
st.subheader("Protected Client", help="Enables or Disables Protected Client, Runs applications inside AppContainer Isolation execution environment. Visit https://learn.microsoft.com/en-us/windows/win32/secauthz/appcontainer-isolation")
protected_client = st.selectbox("Enable Protected Client?", ["Enable", "Disable"])

#Printer Redirection Switch
st.subheader("Printer Redirection", help="Enables or Disables Printer Redirection, allows host to share printers with Sandbox")
printer_redirection = st.selectbox("Enable Printer Redirection?", ["Enable", "Disable"])

#ClipBoard Redirection Switch
st.subheader("Clipboard Redirection", help="Enables or Disables Clipboard Redirection, allows host to share clipboard with Sandbox, and vice versa")
clipboard_redirection = st.selectbox("Enable Clipbpard Redirection?", ["Enable", "Disable"])

#Memorb in MiB Definition
st.subheader("Memory in MiB", help="Defines the amount of memory available to the Sandbox, anything under 2048 will be ignored")
memory_in_mib_in = st.text_input("Memory in MiB")


st.html("<hr></hr>") #page break for looks


# XML generation
#Config
configuration = ET.Element("Configuration")

#vGPU
ET.SubElement(configuration, "VGpu").text = vgpu 

#Network 
ET.SubElement(configuration, "Networking").text = networking 

# Mapped Folder Block
if st.session_state.mapped_folders:
    mapped_folders = ET.SubElement(configuration, "MappedFolders")
    for idx, folder in enumerate(st.session_state.mapped_folders):
        mapped_folder = ET.SubElement(mapped_folders, "MappedFolder")
        ET.SubElement(mapped_folder, "HostFolder").text = st.session_state[f"host_{idx}"]
        ET.SubElement(mapped_folder, "SandboxFolder").text = st.session_state[f"sandbox_{idx}"]
        ET.SubElement(mapped_folder, "ReadOnly").text = str(st.session_state[f"readonly_{idx}"]).lower()

# Logon Command
logon_command = ET.SubElement(configuration, "LogonCommand")
ET.SubElement(logon_command, "Command").text = logon_command_in

# Audio Input
ET.SubElement(configuration, "AudioInput").text = audio_input_in

# Video Input
ET.SubElement(configuration, "VideoInput").text = video_input_in

# Protected Client
ET.SubElement(configuration, "ProtectedClient").text = protected_client

#Printer Redirection
ET.SubElement(configuration, "PrinterRedirection").text = printer_redirection

#Clipboard Redirection
ET.SubElement(configuration, "ClipboardRedirection").text = clipboard_redirection

#Memory in MIB
ET.SubElement(configuration,"MemoryInMB").text = memory_in_mib_in


# Convert to XML string with proper formatting
xml_string = '<?xml version="1.0" encoding="UTF-8"?>\n' + ET.tostring(configuration, encoding="unicode")
xml_pretty = xml.dom.minidom.parseString(xml_string).toprettyxml(indent="  ")

# Display XML output
st.subheader("Generated XML:")
st.code(xml_pretty, language="xml")

# Download button
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