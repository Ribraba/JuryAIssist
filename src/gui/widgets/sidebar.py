"""
Widget de sidebar selon le design Figma.

Contient:
- Titre "JuryAIssist"
- Barre de recherche
- Liste des transcriptions (avec radio buttons)
- Section Library (Import, Paramètres)

Principes SOLID:
- Single Responsibility: Gère uniquement la navigation et la liste des fichiers
- Open/Closed: Extensible via ajout de nouvelles sections
- Interface Segregation: Signaux ciblés pour chaque action
- Dependency Inversion: Ne dépend pas des implémentations concrètes
- Tell, Don't Ask: Les actions sont commandées via signaux
"""
from typing import List, Optional
from PyQt5.QtCore import Qt, pyqtSignal, QSize
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QRadioButton,
    QButtonGroup,
    QScrollArea,
    QFrame,
)

from src.gui.resources import get_icon, get_font
from src.gui.theme import AppSpacing


class SidebarWidget(QWidget):
    """
    Sidebar de navigation selon le design Figma.

    Signals:
        search_changed: Émis quand le texte de recherche change
        file_selected: Émis quand un fichier est sélectionné (nom du fichier)
        import_clicked: Émis quand "Nouvel import" est cliqué
        settings_clicked: Émis quand "Paramètres" est cliqué
    """

    search_changed = pyqtSignal(str)
    file_selected = pyqtSignal(str)
    import_clicked = pyqtSignal()
    settings_clicked = pyqtSignal()

    SIDEBAR_WIDTH = 256

    def __init__(self, parent: Optional[QWidget] = None):
        """
        Initialise la sidebar.

        Args:
            parent: Widget parent
        """
        super().__init__(parent)

        # Configuration
        self.setObjectName("sidebar")
        self.setFixedWidth(self.SIDEBAR_WIDTH)

        # Layout principal
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(AppSpacing.MD, AppSpacing.MD, AppSpacing.MD, AppSpacing.MD)
        main_layout.setSpacing(AppSpacing.LG)

        # 1. Titre de l'app
        self._create_title(main_layout)

        # 2. Barre de recherche
        self._create_search_bar(main_layout)

        # 3. Section Transcriptions
        self._create_transcriptions_section(main_layout)

        # 4. Section Library
        self._create_library_section(main_layout)

        # Spacer pour pousser le contenu vers le haut
        main_layout.addStretch()

    def _create_title(self, layout: QVBoxLayout):
        """
        Crée le titre de l'application.

        Args:
            layout: Layout parent
        """
        title_label = QLabel("JuryAIssist")
        title_label.setObjectName("sidebarTitle")
        title_label.setFont(get_font(20, 600))
        layout.addWidget(title_label)

    def _create_search_bar(self, layout: QVBoxLayout):
        """
        Crée la barre de recherche.

        Args:
            layout: Layout parent
        """
        # Container pour la recherche
        search_container = QWidget()
        search_layout = QHBoxLayout(search_container)
        search_layout.setContentsMargins(0, 0, 0, 0)
        search_layout.setSpacing(AppSpacing.SM)

        # Icône de recherche
        search_icon_label = QLabel()
        search_icon = get_icon("loupe")
        search_icon_label.setPixmap(search_icon.pixmap(QSize(24, 24)))
        search_layout.addWidget(search_icon_label)

        # Champ de recherche
        self._search_input = QLineEdit()
        self._search_input.setObjectName("searchBar")
        self._search_input.setPlaceholderText("Rechercher")
        self._search_input.setFont(get_font(16, 500))
        self._search_input.textChanged.connect(self.search_changed.emit)
        search_layout.addWidget(self._search_input, 1)

        layout.addWidget(search_container)

    def _create_transcriptions_section(self, layout: QVBoxLayout):
        """
        Crée la section "Transcriptions".

        Args:
            layout: Layout parent
        """
        # Titre de section
        section_title = QLabel("Transcriptions")
        section_title.setObjectName("menuSectionTitle")
        section_title.setFont(get_font(16, 600))
        section_title.setStyleSheet("color: #000000;")
        layout.addWidget(section_title)

        # Container scrollable pour la liste
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setFrameShape(QFrame.NoFrame)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll_area.setMaximumHeight(200)  # Limiter la hauteur pour ne pas prendre trop de place
        scroll_area.setStyleSheet("background-color: transparent;")

        # Widget contenant la liste
        self._transcripts_container = QWidget()
        self._transcripts_container.setStyleSheet("background-color: transparent;")
        self._transcripts_layout = QVBoxLayout(self._transcripts_container)
        self._transcripts_layout.setContentsMargins(0, 0, 0, 0)
        self._transcripts_layout.setSpacing(AppSpacing.XS)

        # Button group pour les radio buttons
        self._file_button_group = QButtonGroup(self)
        self._file_button_group.buttonClicked.connect(self._on_file_selected)

        scroll_area.setWidget(self._transcripts_container)
        layout.addWidget(scroll_area, 0)  # Ne pas prendre tout l'espace restant

    def _create_library_section(self, layout: QVBoxLayout):
        """
        Crée la section "Actions".

        Args:
            layout: Layout parent
        """
        # Titre de section
        section_title = QLabel("Actions")
        section_title.setObjectName("menuSectionTitle")
        section_title.setFont(get_font(16, 600))
        section_title.setStyleSheet("color: #000000;")
        layout.addWidget(section_title)

        # Bouton "Nouvel import"
        import_btn = self._create_menu_button("dossier", "Nouvel import")
        import_btn.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                border: none;
                border-radius: 8px;
                text-align: left;
                padding: 8px;
            }
            QPushButton:hover {
                background-color: #fafafa;
            }
        """)
        import_btn.clicked.connect(self.import_clicked.emit)
        layout.addWidget(import_btn)

        # Bouton "Paramètres"
        settings_btn = self._create_menu_button("engrenage", "Paramètres")
        settings_btn.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                border: none;
                border-radius: 8px;
                text-align: left;
                padding: 8px;
            }
            QPushButton:hover {
                background-color: #fafafa;
            }
        """)
        settings_btn.clicked.connect(self.settings_clicked.emit)
        layout.addWidget(settings_btn)

    def _create_menu_button(self, icon_name: str, text: str) -> QPushButton:
        """
        Crée un bouton de menu avec icône.

        Args:
            icon_name: Nom de l'icône
            text: Texte du bouton

        Returns:
            QPushButton configuré
        """
        btn = QPushButton()
        btn.setObjectName("menuItem")

        # Layout horizontal pour icône + texte
        btn_layout = QHBoxLayout(btn)
        btn_layout.setContentsMargins(AppSpacing.SM, 2, AppSpacing.SM, 2)
        btn_layout.setSpacing(AppSpacing.XS)  # Espacement réduit entre icône et texte

        # Icône
        icon_label = QLabel()
        icon_label.setObjectName("menuIcon")
        icon_label.setFixedSize(24, 24)  # Taille réduite pour s'adapter à la ligne
        icon = get_icon(icon_name)
        if not icon.isNull():
            icon_label.setPixmap(icon.pixmap(QSize(20, 20)))
            icon_label.setScaledContents(False)  # Ne pas étirer, centrer le pixmap
            icon_label.setAlignment(Qt.AlignTop | Qt.AlignHCenter)  # Centrer l'icône
        else:
            icon_label.setText("?")  # Debug: montrer si l'icône n'est pas chargée
        btn_layout.addWidget(icon_label)

        # Texte
        text_label = QLabel(text)
        text_label.setObjectName("menuText")
        text_label.setFont(get_font(16, 500))
        text_label.setStyleSheet("color: #000000;")  # Forcer le texte en noir
        text_label.setAlignment(Qt.AlignVCenter | Qt.AlignLeft)  # Alignement vertical centré
        btn_layout.addWidget(text_label, 1)

        # Style
        btn.setFlat(True)
        btn.setCursor(Qt.PointingHandCursor)

        return btn

    def add_transcript_file(self, filename: str, selected: bool = False):
        """
        Ajoute un fichier de transcription à la liste.

        Args:
            filename: Nom du fichier
            selected: Si True, sélectionne ce fichier
        """
        # Container pour le radio button (hauteur fixe compacte)
        file_widget = QWidget()
        file_widget.setFixedHeight(40)  # Hauteur fixe comme dans Figma
        file_layout = QHBoxLayout(file_widget)
        file_layout.setContentsMargins(AppSpacing.SM, AppSpacing.SM, AppSpacing.SM, AppSpacing.SM)
        file_layout.setSpacing(AppSpacing.SM)

        # Radio button (icône)
        radio_icon_label = QLabel()
        radio_icon = get_icon("radio")
        if not radio_icon.isNull():
            radio_icon_label.setPixmap(radio_icon.pixmap(QSize(16, 16)))  # Icône plus petite
            radio_icon_label.setFixedSize(16, 16)
        file_layout.addWidget(radio_icon_label)

        # Radio button (invisible, pour la logique)
        radio_btn = QRadioButton(filename)
        radio_btn.setFont(get_font(16, 500))
        radio_btn.setChecked(selected)
        radio_btn.setObjectName(filename)
        file_layout.addWidget(radio_btn, 1)

        # Ajouter au button group
        self._file_button_group.addButton(radio_btn)

        # Style du container et du radio button
        file_widget.setObjectName("menuItem")
        if selected:
            file_widget.setStyleSheet("""
                #menuItem {
                    background-color: #f7f7f7;
                    border-radius: 8px;
                }
                QRadioButton {
                    color: #000000;
                }
            """)
        else:
            file_widget.setStyleSheet("""
                #menuItem {
                    background-color: transparent;
                    border-radius: 8px;
                }
                #menuItem:hover {
                    background-color: #fafafa;
                }
                QRadioButton {
                    color: #000000;
                }
            """)

        # Ajouter au layout EN HAUT (index 0) pour que les nouveaux fichiers apparaissent en premier
        self._transcripts_layout.insertWidget(0, file_widget)

    def clear_transcript_files(self):
        """Efface tous les fichiers de transcription."""
        # Supprimer tous les widgets
        while self._transcripts_layout.count():
            item = self._transcripts_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        # Vider le button group
        for btn in self._file_button_group.buttons():
            self._file_button_group.removeButton(btn)

    def set_transcript_files(self, filenames: List[str], selected_index: int = 0):
        """
        Définit la liste des fichiers de transcription.

        Args:
            filenames: Liste des noms de fichiers
            selected_index: Index du fichier sélectionné par défaut
        """
        self.clear_transcript_files()

        for i, filename in enumerate(filenames):
            self.add_transcript_file(filename, selected=(i == selected_index))

    def _on_file_selected(self, button: QRadioButton):
        """
        Appelé quand un fichier est sélectionné.

        Args:
            button: Bouton radio sélectionné
        """
        filename = button.text()
        self.file_selected.emit(filename)

        # Mettre à jour le style visuel
        for i in range(self._transcripts_layout.count()):
            widget = self._transcripts_layout.itemAt(i).widget()
            if widget:
                # Chercher le radio button dans ce widget
                radio_btn = widget.findChild(QRadioButton)
                if radio_btn:
                    if radio_btn.isChecked():
                        widget.setStyleSheet("""
                            #menuItem {
                                background-color: #f7f7f7;
                                border-radius: 8px;
                            }
                            QRadioButton {
                                color: #000000;
                            }
                        """)
                    else:
                        widget.setStyleSheet("""
                            #menuItem {
                                background-color: transparent;
                                border-radius: 8px;
                            }
                            #menuItem:hover {
                                background-color: #fafafa;
                            }
                            QRadioButton {
                                color: #000000;
                            }
                        """)

    def get_search_text(self) -> str:
        """
        Retourne le texte de recherche actuel.

        Returns:
            Texte de recherche
        """
        return self._search_input.text()

    def clear_search(self):
        """Efface le texte de recherche."""
        self._search_input.clear()
