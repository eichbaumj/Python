import sys
import os
import sqlite3
import shutil
import tempfile
import plistlib
import hashlib
import base64
from datetime import datetime

from PyQt6.QtCore import (
    Qt,
    QThread,
    pyqtSignal,
    QUrl,
    QByteArray
)
from PyQt6.QtGui import (
    QIcon,
    QPixmap,
    QAction,
    QActionGroup,
    QDesktopServices
)
from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QLabel,
    QLineEdit,
    QPushButton,
    QFileDialog,
    QTextEdit,
    QVBoxLayout,
    QHBoxLayout,
    QGridLayout,
    QProgressBar,
    QMenu,
    QDialog,
    QFrame,
    QGroupBox,
    QFormLayout,
    QPlainTextEdit
)

# --------------------------------------------------------------------
# Embedded Icon (base64 encoded)
# Replace the string below with the actual base64 encoding of icon.ico.
ICON_BASE64 = ("iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsIAAA7CARUoSoAAAAJeSURBVDhPlVNNaBNBFH5vNtk0iiCt4EWDRXrwIhT7Ay2hYEVDq4I/QQXRS1sQq7d4KIonL0qVgnoQ0YOKggjSWy8eRESqKHoQRcEqhSZQW9ukTTa7O89vJhuVetEPvpl533tv3sybXSZAzm9bJWFwipibKdREMcXkh1+JeBzrYasZOIoolA984e2YnG1NURA22g10rvUGNyYGqRzYOIo7JIvVKVJ0jte4d6ga1nSDhPH570jLGAWJ+0qyWYeqqo8W4fRjNVYdQyYvVqUFIfJgGz2Mk8yJpuLSdXXpzS115UWZ9cn2Jhwtjx1fgg9slTiO6us8iQo46TwSz78IdZqSjkP5+Ul19+NzrXWjUmqO9Im2jXI6LXqwY6dN/gN6qHO/8clQdyqSSEQakDwJ9hs7xmGCqYp2he6APt7dY6Ni5ir+F/bULLkuSeA3Qf1mXNigi5nbMSOL0KYyRkPlZjneMFJjYoTCWI58Xivz/hMuzn4ywQZItol1KKpgDNCkZcwlNKxOT5F8X5pQ95728sP3JRsNoDKcv4FuJXFZHNOTnHjcYVnhTrz3ATXxegZ3zYFtUfzf0JnMBtnXLzqz/XAk/QISd5mKmDdHktGORFra2IrL5ZIshxXi5GW9I3MV31wSztXgMPzrTBAwCvsmeBtr86QGBTviQqx7+gq6d09JN7ekdbG4HgVeIbgAHjLVVgL6NCbXbmCgu3YPYKMUHC1w/IiCpsCjZr0S0M9EqWT/BQOIezGNguPgDGiO+Aw8CNYheMbP4OPIts/iIPkYeA3rTZH870DiFnBrZP4niH4CzeVzFl4hey8AAAAASUVORK5CYII=")

def get_embedded_icon():
    """Return a QIcon created from the embedded base64 icon data."""
    icon_bytes = base64.b64decode(ICON_BASE64)
    pixmap = QPixmap()
    pixmap.loadFromData(icon_bytes)
    return QIcon(pixmap)

############################################
# Product Type → Model Dictionary
############################################
PRODUCT_TYPE_MAP = {
    "i386": "iPhone Simulator",
    "x86_64": "iPhone Simulator",
    "arm64": "iPhone Simulator",
    "iPhone1,1": "iPhone",
    "iPhone1,2": "iPhone 3G",
    "iPhone2,1": "iPhone 3GS",
    "iPhone3,1": "iPhone 4",
    "iPhone3,2": "iPhone 4 (GSM Rev A)",
    "iPhone3,3": "iPhone 4 (CDMA)",
    "iPhone4,1": "iPhone 4S",
    "iPhone5,1": "iPhone 5 (GSM)",
    "iPhone5,2": "iPhone 5 (GSM+CDMA)",
    "iPhone5,3": "iPhone 5C (GSM)",
    "iPhone5,4": "iPhone 5C (Global)",
    "iPhone6,1": "iPhone 5S (GSM)",
    "iPhone6,2": "iPhone 5S (Global)",
    "iPhone7,1": "iPhone 6 Plus",
    "iPhone7,2": "iPhone 6",
    "iPhone8,1": "iPhone 6s",
    "iPhone8,2": "iPhone 6s Plus",
    "iPhone8,4": "iPhone SE (GSM)",
    "iPhone9,1": "iPhone 7",
    "iPhone9,2": "iPhone 7 Plus",
    "iPhone9,3": "iPhone 7",
    "iPhone9,4": "iPhone 7 Plus",
    "iPhone10,1": "iPhone 8",
    "iPhone10,2": "iPhone 8 Plus",
    "iPhone10,3": "iPhone X (Global)",
    "iPhone10,4": "iPhone 8",
    "iPhone10,5": "iPhone 8 Plus",
    "iPhone10,6": "iPhone X (GSM)",
    "iPhone11,2": "iPhone XS",
    "iPhone11,4": "iPhone XS Max",
    "iPhone11,6": "iPhone XS Max (Global)",
    "iPhone11,8": "iPhone XR",
    "iPhone12,1": "iPhone 11",
    "iPhone12,3": "iPhone 11 Pro",
    "iPhone12,5": "iPhone 11 Pro Max",
    "iPhone12,8": "iPhone SE (2nd Gen)",
    "iPhone13,1": "iPhone 12 Mini",
    "iPhone13,2": "iPhone 12",
    "iPhone13,3": "iPhone 12 Pro",
    "iPhone13,4": "iPhone 12 Pro Max",
    "iPhone14,2": "iPhone 13 Pro",
    "iPhone14,3": "iPhone 13 Pro Max",
    "iPhone14,4": "iPhone 13 Mini",
    "iPhone14,5": "iPhone 13",
    "iPhone14,6": "iPhone SE (3rd Gen)",
    "iPhone14,7": "iPhone 14",
    "iPhone14,8": "iPhone 14 Plus",
    "iPhone15,2": "iPhone 14 Pro",
    "iPhone15,3": "iPhone 14 Pro Max",
    "iPhone15,4": "iPhone 15",
    "iPhone15,5": "iPhone 15 Plus",
    "iPhone16,1": "iPhone 15 Pro",
    "iPhone16,2": "iPhone 15 Pro Max",
    "iPhone17,1": "iPhone 16 Pro",
    "iPhone17,2": "iPhone 16 Pro Max",
    "iPhone17,3": "iPhone 16",
    "iPhone17,4": "iPhone 16 Plus",
    "iPhone17,5": "iPhone 16e",
}


############################################
# Worker Thread for Reconstruction
############################################
class ReconstructionWorker(QThread):
    status_signal = pyqtSignal(str)
    progress_signal = pyqtSignal(int)
    finished_signal = pyqtSignal(str)

    def __init__(self, backup_path, output_path, plist_info, hash_algorithm="sha256"):
        super().__init__()
        self.backup_path = backup_path
        self.output_path = output_path
        self.plist_info = plist_info
        self.hash_algorithm = hash_algorithm  # "md5", "sha1", or "sha256"
        self.temp_log_path = None
        self._cancelled = False
        self._paused = False

    def cancel(self):
        self._cancelled = True

    def pause(self):
        self._paused = True

    def resume(self):
        self._paused = False

    def log_to_temp(self, message: str):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(self.temp_log_path, 'a', encoding='utf-8') as f:
            f.write(f"[{timestamp}] {message}\n")

    def compute_file_hash(self, file_path):
        """Compute the file hash using the selected algorithm."""
        if self.hash_algorithm == "sha256":
            h = hashlib.sha256()
        elif self.hash_algorithm == "sha1":
            h = hashlib.sha1()
        elif self.hash_algorithm == "md5":
            h = hashlib.md5()
        else:
            h = hashlib.sha256()
        with open(file_path, "rb") as f:
            for byte_block in iter(lambda: f.read(4096), b""):
                h.update(byte_block)
        return h.hexdigest()

    def run(self):
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".txt")
        self.temp_log_path = temp_file.name
        temp_file.close()

        start_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.log_to_temp(f"Normalization process started at {start_time}")
        self.status_signal.emit(f"Normalization started at {start_time}")

        manifest_db_path = os.path.join(self.backup_path, "Manifest.db")
        self.status_signal.emit(f"Debug: manifest_db_path = {manifest_db_path}")
        self.log_to_temp(f"Debug: manifest_db_path = {manifest_db_path}")

        if not os.path.isfile(manifest_db_path):
            msg = f"Error: Manifest.db not found at {manifest_db_path}"
            self.status_signal.emit(msg)
            self.log_to_temp(msg)
            self.finished_signal.emit(self.temp_log_path)
            return

        if not os.path.exists(self.backup_path):
            msg = f"Error: Backup path not found at {self.backup_path}"
            self.status_signal.emit(msg)
            self.log_to_temp(msg)
            self.finished_signal.emit(self.temp_log_path)
            return

        if not os.access(self.output_path, os.W_OK):
            try:
                os.makedirs(self.output_path, exist_ok=True)
            except Exception as e:
                msg = f"Error: Destination folder {self.output_path} is not writable or cannot be created. {e}"
                self.status_signal.emit(msg)
                self.log_to_temp(msg)
                self.finished_signal.emit(self.temp_log_path)
                return

        try:
            with sqlite3.connect(manifest_db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT fileID, domain, relativePath FROM Files")
                rows = cursor.fetchall()
                self.status_signal.emit("Successfully executed SQL query on Manifest.db.")
                self.log_to_temp("Successfully executed SQL query on Manifest.db.")
        except sqlite3.Error as e:
            msg = f"Error executing SQL on Manifest.db: {e}"
            self.status_signal.emit(msg)
            self.log_to_temp(msg)
            self.finished_signal.emit(self.temp_log_path)
            return

        total_files = len(rows)
        self.status_signal.emit(f"Found {total_files} files to process...")
        self.log_to_temp(f"Found {total_files} files to process...")

        for i, (fileID, domain, relativePath) in enumerate(rows, start=1):
            while self._paused and not self._cancelled:
                self.msleep(200)
            if self._cancelled:
                cancel_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                self.status_signal.emit("Normalization cancelled by user.")
                self.log_to_temp(f"Normalization cancelled by user at {cancel_time}")
                break
            try:
                source_file = self.get_backup_file_path(self.backup_path, fileID)
                destination_file = self.get_output_path(self.output_path, domain, relativePath)
                os.makedirs(os.path.dirname(destination_file), exist_ok=True)

                if os.path.exists(source_file):
                    shutil.copy2(source_file, destination_file)
                    hash_value = self.compute_file_hash(destination_file)
                    self.log_to_temp(f"Copied: {source_file} -> {destination_file}, {self.hash_algorithm.upper()} hash: {hash_value}")
                else:
                    self.log_to_temp(f"Warning: Source file not found: {source_file}")
            except Exception as e:
                self.log_to_temp(f"Error processing fileID {fileID}: {e}")

            percent_done = int((i / total_files) * 100)
            self.progress_signal.emit(percent_done)

        end_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.log_to_temp(f"Normalization complete at {end_time}")
        if not self._cancelled:
            self.status_signal.emit(f"Normalization complete at {end_time}")
        self.finished_signal.emit(self.temp_log_path)

    @staticmethod
    def get_backup_file_path(backup_path, file_id):
        return os.path.join(backup_path, file_id[:2], file_id)

    @staticmethod
    def get_output_path(base_folder, domain, relative_path):
        domain_mappings = {
            "AppDomain-": "private/var/mobile/Containers/Data/Application",
            "AppDomainGroup-": "private/var/mobile/Containers/Shared/AppGroup",
            "AppDomainPlugin-": "private/var/mobile/Containers/Data/PluginKitPlugin",
            "CameraRollDomain": "private/var/mobile",
            "DatabaseDomain": "private/var/db",
            "HealthDomain": "private/var/mobile/Library/Health",
            "HomeDomain": "private/var/mobile",
            "HomeKitDomain": "private/var/mobile/",
            "InstallDomain": "private/var/installld",
            "KeyboardDomain": "private/var/mobile",
            "KeychainDomain": "private/var/Keychains",
            "ManagedPreferencesDomain": "private/var/Managed Preferences",
            "MediaDomain": "private/var/mobile/Media",
            "MobileDeviceDomain": "private/var/MobileDevice",
            "NetworkDomain": "private/var/networkd",
            "ProtectedDomain": "private/var/protected",
            "RootDomain": "private/var/root",
            "SysContainerDomain-": "private/var/containers/Data/System",
            "SysSharedContainerDomain-": "private/var/containers/Shared/SystemGroup",
            "SystemPreferencesDomain": "private/var/preferences/",
            "TonesDomain": "private/var/mobile",
            "WirelessDomain": "private/var/wireless"
        }

        base_path = None
        for prefix, path in domain_mappings.items():
            if domain.startswith(prefix):
                base_path = os.path.join(base_folder, path)
                if prefix in ["AppDomain-", "AppDomainGroup-", "AppDomainPlugin-", "SysContainerDomain-", "SysSharedContainerDomain-"]:
                    app_name = domain[len(prefix):]
                    base_path = os.path.join(base_path, app_name)
                break

        if base_path is None:
            base_path = os.path.join(base_folder, "private/var/Other")

        return os.path.join(base_path, relative_path)


############################################
# Main Window
############################################
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Set overall window size to 1000x600
        self.setMinimumSize(1200, 600)
        self.setWindowTitle("Backup2FS")
        self.setWindowIcon(get_embedded_icon())

        # Default hash algorithm
        self.hash_algorithm = "sha256"

        # --- Menu Bar ---
        self.menu_bar = self.menuBar()
        # File Menu
        file_menu = QMenu("File", self)
        self.menu_bar.addMenu(file_menu)
        exit_action = QAction("Exit", self)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        # Options Menu
        options_menu = QMenu("Options", self)
        self.menu_bar.addMenu(options_menu)
        # Hashing Submenu
        hashing_menu = QMenu("Hashing", self)
        options_menu.addMenu(hashing_menu)
        self.hashing_action_group = QActionGroup(self)
        self.hashing_action_group.setExclusive(True)

        action_md5 = QAction("MD5", self, checkable=True)
        action_sha1 = QAction("SHA1", self, checkable=True)
        action_sha256 = QAction("SHA256", self, checkable=True)
        action_sha256.setChecked(True)  # Default selection

        self.hashing_action_group.addAction(action_md5)
        self.hashing_action_group.addAction(action_sha1)
        self.hashing_action_group.addAction(action_sha256)

        hashing_menu.addAction(action_md5)
        hashing_menu.addAction(action_sha1)
        hashing_menu.addAction(action_sha256)

        action_md5.triggered.connect(lambda: self.set_hash_algorithm("md5"))
        action_sha1.triggered.connect(lambda: self.set_hash_algorithm("sha1"))
        action_sha256.triggered.connect(lambda: self.set_hash_algorithm("sha256"))

        # Help Menu
        help_menu = QMenu("Help", self)
        self.menu_bar.addMenu(help_menu)
        about_action = QAction("About", self)
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)

        # Create the central widget and overall layout (horizontal split)
        container = QWidget()
        self.setCentralWidget(container)

        # --------------------
        # Left Panel: Backup Details (Vital Info)
        # Two group boxes: "Details" and "Installed Apps"
        self.detailsGroup = QGroupBox("Details")
        self.appsGroup = QGroupBox("Installed Apps")

        # --- Details Group Layout ---
        detailsLayout = QFormLayout()
        self.deviceNameValue = QLabel("")
        self.modelValue = QLabel("")
        self.iosVersionValue = QLabel("")
        self.buildVersionValue = QLabel("")
        self.serialNumberValue = QLabel("")
        self.uniqueIDValue = QLabel("")
        self.imeiValue = QLabel("")
        self.encryptedValue = QLabel("")

        detailsLayout.addRow("Device Name:", self.deviceNameValue)
        detailsLayout.addRow("Model:", self.modelValue)
        detailsLayout.addRow("iOS Version:", self.iosVersionValue)
        detailsLayout.addRow("Build Version:", self.buildVersionValue)
        detailsLayout.addRow("Serial Number:", self.serialNumberValue)
        detailsLayout.addRow("Unique Device ID:", self.uniqueIDValue)
        detailsLayout.addRow("IMEI:", self.imeiValue)
        detailsLayout.addRow("Encrypted:", self.encryptedValue)
        self.detailsGroup.setLayout(detailsLayout)

        # --- Apps Group Layout ---
        appsLayout = QVBoxLayout()
        self.appsText = QPlainTextEdit()
        self.appsText.setReadOnly(True)
        self.appsText.setMinimumHeight(100)
        appsLayout.addWidget(self.appsText)
        self.appsGroup.setLayout(appsLayout)

        # Stack the two group boxes vertically in the left panel
        leftLayout = QVBoxLayout()
        leftLayout.addWidget(self.detailsGroup)
        leftLayout.addWidget(self.appsGroup)

        # Wrap left layout in a frame with fixed width
        self.vitalFrame = QFrame()
        self.vitalFrame.setFrameShape(QFrame.Shape.Box)
        self.vitalFrame.setFrameShadow(QFrame.Shadow.Raised)
        self.vitalFrame.setLayout(leftLayout)
        self.vitalFrame.setFixedWidth(340)

        # --------------------
        # Right Panel: Main Controls and Log
        # --------------------
        self.titleLabel = QLabel("iOS Backup Normalizer")
        self.titleLabel.setStyleSheet("font-size: 20px; font-weight: bold;")

        self.backupLabel = QLabel("Backup Folder")
        self.backupLineEdit = QLineEdit()
        self.backupSelectBtn = QPushButton("Select")
        self.backupSelectBtn.setObjectName("browseButton")
        self.backupSelectBtn.clicked.connect(self.browse_backup_folder)

        self.outputLabel = QLabel("Destination Folder")
        self.outputLineEdit = QLineEdit()
        self.outputSelectBtn = QPushButton("Select")
        self.outputSelectBtn.setObjectName("browseButton")
        self.outputSelectBtn.clicked.connect(self.browse_output_folder)

        self.createButton = QPushButton("Normalize")
        self.createButton.setObjectName("createButton")
        self.createButton.clicked.connect(self.on_create_clicked)

        self.logTextEdit = QTextEdit()
        self.logTextEdit.setReadOnly(True)

        self.progressBar = QProgressBar()
        self.progressBar.setRange(0, 100)
        self.progressBar.setValue(0)
        self.progressBar.setFormat("%p%")
        self.progressBar.setStyleSheet("""
            QProgressBar {
                border: 1px solid #000;
                text-align: center;
            }
            QProgressBar::chunk {
                background-color: #00cc00;
                width: 1px;
            }
        """)

        self.cancelButton = QPushButton("Cancel")
        self.cancelButton.setObjectName("cancelButton")
        self.cancelButton.clicked.connect(self.on_cancel_clicked)

        self.pauseResumeButton = QPushButton("Pause")
        self.pauseResumeButton.setObjectName("pauseResumeButton")
        self.pauseResumeButton.clicked.connect(self.on_pause_resume_clicked)
        self.pauseResumeButton.setEnabled(False)

        self.saveLogButton = QPushButton("Save Log")
        self.saveLogButton.setObjectName("saveLogButton")
        self.saveLogButton.clicked.connect(self.save_log)
        self.saveLogButton.setEnabled(False)

        # New "Open Folder" button - initially hidden
        self.openFolderButton = QPushButton("Open Folder")
        self.openFolderButton.setObjectName("openFolderButton")
        self.openFolderButton.clicked.connect(self.open_folder)
        self.openFolderButton.setVisible(False)

        self.topFrame = QFrame()
        self.topFrame.setFrameShape(QFrame.Shape.Box)
        self.topFrame.setFrameShadow(QFrame.Shadow.Raised)
        topFrameLayout = QGridLayout()
        topFrameLayout.addWidget(self.backupLabel, 0, 0)
        topFrameLayout.addWidget(self.backupLineEdit, 0, 1)
        topFrameLayout.addWidget(self.backupSelectBtn, 0, 2)
        topFrameLayout.addWidget(self.outputLabel, 1, 0)
        topFrameLayout.addWidget(self.outputLineEdit, 1, 1)
        topFrameLayout.addWidget(self.outputSelectBtn, 1, 2)
        topFrameLayout.addWidget(self.createButton, 2, 1)
        self.topFrame.setLayout(topFrameLayout)

        self.bottomFrame = QFrame()
        self.bottomFrame.setFrameShape(QFrame.Shape.Box)
        self.bottomFrame.setFrameShadow(QFrame.Shadow.Raised)
        bottomFrameLayout = QVBoxLayout()
        bottomFrameLayout.addWidget(self.logTextEdit)
        bottomFrameLayout.addWidget(self.progressBar)
        
        # Bottom row: Center the Open Folder button and place other buttons on the right.
        bottomButtonLayout = QHBoxLayout()
        bottomButtonLayout.addStretch()
        bottomButtonLayout.addStretch()
        bottomButtonLayout.addWidget(self.pauseResumeButton)
        bottomButtonLayout.addWidget(self.cancelButton)
        bottomButtonLayout.addWidget(self.saveLogButton)
        bottomButtonLayout.addWidget(self.openFolderButton)
        bottomFrameLayout.addLayout(bottomButtonLayout)
        self.bottomFrame.setLayout(bottomFrameLayout)

        # Right side vertical layout
        rightLayout = QVBoxLayout()
        titleLayout = QHBoxLayout()
        titleLayout.addWidget(self.titleLabel)
        titleLayout.addStretch()
        rightLayout.addLayout(titleLayout)
        rightLayout.addWidget(self.topFrame)
        rightLayout.addWidget(self.bottomFrame)

        # Main horizontal layout: Left Panel (vitalFrame) and Right Panel (Controls/Log)
        mainLayout = QHBoxLayout()
        mainLayout.addWidget(self.vitalFrame)
        mainLayout.addLayout(rightLayout)
        mainLayout.setContentsMargins(10, 10, 10, 10)
        container.setLayout(mainLayout)

        # Overall stylesheet
        self.setStyleSheet("""
            QMainWindow {
                background-color: #121E2B;
            }
            QLabel {
                color: #FFFFFF;
            }
            QGroupBox {
                color: #FFFFFF;
                border: 1px solid #FFFFFF;
                margin-top: 6px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                subcontrol-position: top left;
                padding: 0 3px;
            }
            QLineEdit {
                background-color: #FFFFFF;
                color: #000000;
                border: 1px solid #000000;
            }
            QTextEdit, QPlainTextEdit {
                background-color: #FFFFFF;
                color: #000000;
                border: 1px solid #000000;
            }
            QPushButton {
                background-color: #EE3D53;
                color: #FFFFFF;
                border: none;
                border-radius: 8px;
                padding: 6px 12px;
                font-size: 14px;
                outline: 0;
            }
            QPushButton:hover {
                background-color: #F37934;
            }
            QPushButton:focus {
                outline: none;
            }
            #browseButton, #createButton {
                background-color: #F37934;
            }
            #browseButton:hover, #createButton:hover {
                background-color: #EE3D53;
            }
            #saveLogButton {
                background-color: #EE3D53;
            }
            #saveLogButton:hover {
                background-color: #F37934;
            }
            #openFolderButton {
                background-color: #F37934;
            }
            #openFolderButton:hover {
                background-color: #EE3D53;
            }
        """)

        reconstruct_btn_width = max(
            self.saveLogButton.sizeHint().width(),
            self.createButton.sizeHint().width()
        )
        self.createButton.setFixedWidth(reconstruct_btn_width)

        self.temp_log_path = None

    def log_message(self, message: str):
        """Append a message with a timestamp to the log window."""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.logTextEdit.append(f"[{timestamp}] {message}")

    def set_hash_algorithm(self, algorithm):
        self.hash_algorithm = algorithm
        self.log_message(f"Hashing algorithm set to {algorithm.upper()}.")

    def browse_backup_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "Select Backup Folder")
        if folder:
            self.backupLineEdit.setText(folder)
            self.update_vital_info()

    def update_vital_info(self):
        """Read Manifest.plist and Info.plist from the selected backup folder
           and update the left panel (Details + Installed Apps)."""
        backup_path = self.backupLineEdit.text().strip()
        manifest_plist_path = os.path.join(backup_path, "Manifest.plist")

        # Clear existing info
        self.deviceNameValue.setText("")
        self.modelValue.setText("")
        self.iosVersionValue.setText("")
        self.buildVersionValue.setText("")
        self.serialNumberValue.setText("")
        self.uniqueIDValue.setText("")
        self.imeiValue.setText("")
        self.encryptedValue.setText("")
        self.appsText.clear()

        # Update details from Manifest.plist (if exists)
        if os.path.isfile(manifest_plist_path):
            try:
                with open(manifest_plist_path, 'rb') as f:
                    plist_data = plistlib.load(f)
                is_encrypted = plist_data.get("IsEncrypted", False)
                lockdown_data = plist_data.get("Lockdown", {})
                device_name = lockdown_data.get("DeviceName", "N/A")
                build_version = lockdown_data.get("BuildVersion", "N/A")
                product_type = lockdown_data.get("ProductType", "N/A")
                ios_version = lockdown_data.get("ProductVersion", "N/A")
                serial_number = lockdown_data.get("SerialNumber", "N/A")
                unique_id = lockdown_data.get("UniqueDeviceID", "N/A")
                model_name = PRODUCT_TYPE_MAP.get(product_type, product_type)

                self.deviceNameValue.setText(device_name)
                self.modelValue.setText(model_name)
                self.iosVersionValue.setText(ios_version)
                self.buildVersionValue.setText(build_version)
                self.serialNumberValue.setText(serial_number)
                self.uniqueIDValue.setText(unique_id)
                self.encryptedValue.setText("Yes" if is_encrypted else "No")
            except Exception as e:
                self.deviceNameValue.setText("Error")
                self.modelValue.setText("Error")
                self.iosVersionValue.setText("Error")
                self.buildVersionValue.setText("Error")
                self.serialNumberValue.setText("Error")
                self.uniqueIDValue.setText("Error")
                self.encryptedValue.setText("Error")
        else:
            self.deviceNameValue.setText("Not found")
            self.modelValue.setText("Not found")
            self.iosVersionValue.setText("Not found")
            self.buildVersionValue.setText("Not found")
            self.serialNumberValue.setText("Not found")
            self.uniqueIDValue.setText("Not found")
            self.encryptedValue.setText("N/A")

        # Update additional info from Info.plist (if exists)
        info_plist_path = os.path.join(backup_path, "Info.plist")
        if os.path.isfile(info_plist_path):
            try:
                with open(info_plist_path, 'rb') as f:
                    info_data = plistlib.load(f)
                imei = info_data.get("IMEI", "N/A")
                installed_apps = info_data.get("Installed Applications", [])
                self.imeiValue.setText(str(imei))
                if isinstance(installed_apps, list) and installed_apps:
                    self.appsText.setPlainText("\n".join(installed_apps))
                else:
                    self.appsText.setPlainText("N/A")
            except Exception as e:
                self.imeiValue.setText("Error")
                self.appsText.setPlainText("Error")
        else:
            self.imeiValue.setText("Not found")
            self.appsText.setPlainText("Not found")

    def browse_output_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "Select Destination Folder")
        if folder:
            self.outputLineEdit.setText(folder)

    def on_create_clicked(self):
        self.createButton.setEnabled(False)
        backup_path = self.backupLineEdit.text().strip()
        output_path = self.outputLineEdit.text().strip()

        if not backup_path or not output_path:
            self.log_message("Please select both backup and destination folders.")
            self.createButton.setEnabled(True)
            return

        manifest_plist_path = os.path.join(backup_path, "Manifest.plist")
        if not os.path.isfile(manifest_plist_path):
            self.log_message("Manifest.plist not found. Cannot determine encryption status.")
            self.createButton.setEnabled(True)
            return

        try:
            with open(manifest_plist_path, 'rb') as f:
                plist_data = plistlib.load(f)
        except Exception as e:
            self.log_message(f"Could not read Manifest.plist: {e}")
            self.createButton.setEnabled(True)
            return

        is_encrypted = plist_data.get("IsEncrypted", False)
        if is_encrypted:
            self.log_message("This backup is encrypted. Please decrypt it first.")
            self.createButton.setEnabled(True)
            return

        lockdown_data = plist_data.get("Lockdown", {})
        build_version   = lockdown_data.get("BuildVersion", "")
        device_name     = lockdown_data.get("DeviceName", "")
        product_type    = lockdown_data.get("ProductType", "")
        product_version = lockdown_data.get("ProductVersion", "")
        serial_number   = lockdown_data.get("SerialNumber", "")
        unique_device_id= lockdown_data.get("UniqueDeviceID", "")

        model_name = PRODUCT_TYPE_MAP.get(product_type, product_type)

        self.logTextEdit.clear()
        self.log_message(f"Build number: {build_version}")
        self.log_message(f"Name: {device_name}")
        self.log_message(f"Model: {model_name}")
        self.log_message(f"iOS Version: {product_version}")
        self.log_message(f"Serial Number: {serial_number}")
        self.log_message(f"Unique Device ID: {unique_device_id}")
        self.log_message("-----------------------------------------------------------")

        plist_info = {
            "build_version": build_version,
            "device_name": device_name,
            "product_type": product_type,
            "product_version": product_version,
            "serial_number": serial_number,
            "unique_device_id": unique_device_id
        }

        self.progressBar.setValue(0)
        self.saveLogButton.setEnabled(False)
        self.pauseResumeButton.setEnabled(True)

        # Pass the selected hashing algorithm to the worker.
        self.worker = ReconstructionWorker(backup_path, output_path, plist_info, hash_algorithm=self.hash_algorithm)
        self.worker.status_signal.connect(self.on_status_update)
        self.worker.progress_signal.connect(self.on_progress_update)
        self.worker.finished_signal.connect(self.on_finished)
        self.worker.start()

    def on_status_update(self, message):
        self.log_message(message)

    def on_progress_update(self, percent):
        self.progressBar.setValue(percent)

    def on_finished(self, temp_log_path):
        self.temp_log_path = temp_log_path
        self.saveLogButton.setEnabled(True)
        self.createButton.setEnabled(False)
        self.cancelButton.setEnabled(False)
        self.pauseResumeButton.setEnabled(False)
        self.log_message("Process finished.")
        # Show the Open Folder button when normalization is complete
        self.openFolderButton.setVisible(True)

    def open_folder(self):
        folder = self.outputLineEdit.text().strip()
        if os.path.isdir(folder):
            QDesktopServices.openUrl(QUrl.fromLocalFile(folder))
        else:
            self.log_message("Output folder does not exist.")

    def save_log(self):
        if not self.temp_log_path or not os.path.exists(self.temp_log_path):
            self.log_message("No verbose log found to save.")
            return

        filename, _ = QFileDialog.getSaveFileName(
            self,
            "Save Log",
            "",
            "CSV Files (*.csv);;Text Files (*.txt);;All Files (*)"
        )
        if filename:
            try:
                shutil.copy2(self.temp_log_path, filename)
                self.log_message(f"Full verbose log saved to: {filename}")
            except Exception as e:
                self.log_message(f"Error saving log: {e}")

    def on_cancel_clicked(self):
        if hasattr(self, 'worker') and self.worker.isRunning():
            self.worker.cancel()
            cancel_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            self.log_message(f"Normalization process cancelled at {cancel_time}.")
            self.cancelButton.setEnabled(False)
            self.createButton.setEnabled(False)
            self.pauseResumeButton.setEnabled(False)

    def on_pause_resume_clicked(self):
        if hasattr(self, 'worker') and self.worker.isRunning():
            if not self.worker._paused:
                self.worker.pause()
                pause_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                self.pauseResumeButton.setText("Resume")
                self.log_message(f"Normalization paused at {pause_time}.")
            else:
                self.worker.resume()
                resume_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                self.pauseResumeButton.setText("Pause")
                self.log_message(f"Normalization resumed at {resume_time}.")

    def show_about(self):
        about_dialog = QDialog(self)
        about_dialog.setWindowTitle("About Backup2FS")
        about_dialog.setWindowIcon(get_embedded_icon())
        about_dialog.setStyleSheet("background-color: #1B293B; color: white;")

        about_layout = QVBoxLayout()
        logo_label = QLabel()
        # Using external logo file for About dialog (if present)
        logo_pixmap = QPixmap("logo.png")
        logo_scaled_pixmap = logo_pixmap.scaled(
            500, 72,
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation
        )
        logo_label.setPixmap(logo_scaled_pixmap)
        logo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        about_layout.addWidget(logo_label)

        about_text = QLabel("Backup2FS\n\nNormalizes and converts iOS backups into a standard iOS file-system structure for forensic analysis.\n\nCreated by James Eichbaum\n© Elusive Data 2025")
        about_text.setAlignment(Qt.AlignmentFlag.AlignCenter)
        about_layout.addWidget(about_text)

        about_dialog.setLayout(about_layout)
        about_dialog.setFixedSize(550, 300)
        about_dialog.setAttribute(Qt.WidgetAttribute.WA_DeleteOnClose)
        about_dialog.exec()

    def closeEvent(self, event):
        if self.temp_log_path and os.path.exists(self.temp_log_path):
            try:
                os.remove(self.temp_log_path)
                print(f"Temporary log {self.temp_log_path} removed.")
            except Exception as e:
                print(f"Error cleaning up temporary log: {e}")
        event.accept()


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
