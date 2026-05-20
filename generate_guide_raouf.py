from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    HRFlowable, KeepTogether
)
from reportlab.lib.enums import TA_LEFT, TA_CENTER

OUTPUT = "/mnt/deep-learning/ubuntu-server-network-rtl8192eu/guide-connexion-raouf.pdf"

# ── Couleurs ────────────────────────────────────────────────────────────────
BLEU      = colors.HexColor("#2563EB")
BLEU_CLAIR= colors.HexColor("#DBEAFE")
GRIS_BG   = colors.HexColor("#1E1E2E")
GRIS_CODE = colors.HexColor("#F1F5F9")
VERT      = colors.HexColor("#16A34A")
ROUGE     = colors.HexColor("#DC2626")
GRIS_TEXTE= colors.HexColor("#374151")
BLANC     = colors.white

# ── Styles ──────────────────────────────────────────────────────────────────
styles = getSampleStyleSheet()

s_titre = ParagraphStyle("titre",
    fontSize=24, leading=30, textColor=BLANC,
    fontName="Helvetica-Bold", alignment=TA_CENTER, spaceAfter=4)

s_sous_titre = ParagraphStyle("sous_titre",
    fontSize=12, leading=16, textColor=colors.HexColor("#BFDBFE"),
    fontName="Helvetica", alignment=TA_CENTER, spaceAfter=0)

s_h1 = ParagraphStyle("h1",
    fontSize=14, leading=18, textColor=BLEU,
    fontName="Helvetica-Bold", spaceBefore=16, spaceAfter=6,
    borderPad=0)

s_body = ParagraphStyle("body",
    fontSize=10, leading=15, textColor=GRIS_TEXTE,
    fontName="Helvetica", spaceAfter=4)

s_code = ParagraphStyle("code",
    fontSize=9, leading=14, textColor=colors.HexColor("#1E293B"),
    fontName="Courier", leftIndent=8, spaceAfter=2)

s_note = ParagraphStyle("note",
    fontSize=9, leading=13, textColor=colors.HexColor("#6B7280"),
    fontName="Helvetica-Oblique", spaceAfter=4)

s_badge = ParagraphStyle("badge",
    fontSize=10, leading=14, textColor=BLANC,
    fontName="Helvetica-Bold", alignment=TA_CENTER)

s_step_num = ParagraphStyle("step_num",
    fontSize=18, leading=22, textColor=BLEU,
    fontName="Helvetica-Bold", alignment=TA_CENTER)

s_step_title = ParagraphStyle("step_title",
    fontSize=12, leading=16, textColor=GRIS_TEXTE,
    fontName="Helvetica-Bold")

s_step_body = ParagraphStyle("step_body",
    fontSize=10, leading=14, textColor=GRIS_TEXTE,
    fontName="Helvetica")

s_table_header = ParagraphStyle("th",
    fontSize=9, leading=12, textColor=BLANC,
    fontName="Helvetica-Bold", alignment=TA_CENTER)

s_table_cell = ParagraphStyle("td",
    fontSize=9, leading=12, textColor=GRIS_TEXTE,
    fontName="Courier")

s_table_label = ParagraphStyle("tl",
    fontSize=9, leading=12, textColor=GRIS_TEXTE,
    fontName="Helvetica")

def code_block(lines):
    """Bloc de code avec fond gris."""
    content = [Paragraph(line, s_code) for line in lines]
    tbl = Table([[content]], colWidths=[15.5*cm])
    tbl.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,-1), GRIS_CODE),
        ("ROUNDEDCORNERS", [6]),
        ("LEFTPADDING",  (0,0), (-1,-1), 10),
        ("RIGHTPADDING", (0,0), (-1,-1), 10),
        ("TOPPADDING",   (0,0), (-1,-1), 8),
        ("BOTTOMPADDING",(0,0), (-1,-1), 8),
        ("BOX", (0,0), (-1,-1), 1, colors.HexColor("#CBD5E1")),
    ]))
    return tbl

def step_block(num, title, body_paragraphs):
    """Bloc étape numérotée."""
    num_cell  = Paragraph(str(num), s_step_num)
    title_p   = Paragraph(title, s_step_title)
    content   = [title_p, Spacer(1, 4)] + body_paragraphs
    tbl = Table(
        [[num_cell, content]],
        colWidths=[1.5*cm, 14*cm]
    )
    tbl.setStyle(TableStyle([
        ("VALIGN",        (0,0), (-1,-1), "TOP"),
        ("LEFTPADDING",   (0,0), (0,0),  0),
        ("RIGHTPADDING",  (0,0), (0,0),  10),
        ("LEFTPADDING",   (1,0), (1,0),  0),
        ("TOPPADDING",    (0,0), (-1,-1), 0),
        ("BOTTOMPADDING", (0,0), (-1,-1), 0),
        ("LINEAFTER",     (0,0), (0,-1), 2, BLEU_CLAIR),
    ]))
    wrapper = Table([[tbl]], colWidths=[15.5*cm])
    wrapper.setStyle(TableStyle([
        ("BACKGROUND",    (0,0), (-1,-1), BLANC),
        ("BOX",           (0,0), (-1,-1), 1, colors.HexColor("#E2E8F0")),
        ("LEFTPADDING",   (0,0), (-1,-1), 12),
        ("RIGHTPADDING",  (0,0), (-1,-1), 12),
        ("TOPPADDING",    (0,0), (-1,-1), 10),
        ("BOTTOMPADDING", (0,0), (-1,-1), 10),
    ]))
    return wrapper

# ── Document ────────────────────────────────────────────────────────────────
doc = SimpleDocTemplate(
    OUTPUT, pagesize=A4,
    leftMargin=2.5*cm, rightMargin=2.5*cm,
    topMargin=2*cm, bottomMargin=2*cm
)

story = []

# ── HEADER BANNER ───────────────────────────────────────────────────────────
header_data = [[
    Paragraph("Guide de connexion au serveur Z800", s_titre),
    Paragraph("Accès distant via Tailscale — Pour Raouf", s_sous_titre),
]]
header = Table(header_data, colWidths=[15.5*cm])
header.setStyle(TableStyle([
    ("BACKGROUND",    (0,0), (-1,-1), GRIS_BG),
    ("ROUNDEDCORNERS",[8]),
    ("LEFTPADDING",   (0,0), (-1,-1), 20),
    ("RIGHTPADDING",  (0,0), (-1,-1), 20),
    ("TOPPADDING",    (0,0), (-1,-1), 20),
    ("BOTTOMPADDING", (0,0), (-1,-1), 20),
]))
story.append(header)
story.append(Spacer(1, 18))

# ── INFO BADGES ─────────────────────────────────────────────────────────────
badges = Table([[
    Paragraph("IP du serveur\n100.86.17.82", s_badge),
    Paragraph("Utilisateur SSH\nsamir", s_badge),
    Paragraph("OS\nUbuntu 22.04 LTS", s_badge),
    Paragraph("GPU\nQuadro P4000 8GB", s_badge),
]], colWidths=[3.8*cm]*4, rowHeights=[1.2*cm])
badges.setStyle(TableStyle([
    ("BACKGROUND",    (0,0), (0,0), BLEU),
    ("BACKGROUND",    (1,0), (1,0), VERT),
    ("BACKGROUND",    (2,0), (2,0), colors.HexColor("#7C3AED")),
    ("BACKGROUND",    (3,0), (3,0), colors.HexColor("#D97706")),
    ("ROUNDEDCORNERS",[6]),
    ("LEFTPADDING",   (0,0), (-1,-1), 4),
    ("RIGHTPADDING",  (0,0), (-1,-1), 4),
    ("TOPPADDING",    (0,0), (-1,-1), 6),
    ("BOTTOMPADDING", (0,0), (-1,-1), 6),
    ("VALIGN",        (0,0), (-1,-1), "MIDDLE"),
    ("COLPADDING",    (0,0), (-1,-1), 2),
]))
story.append(badges)
story.append(Spacer(1, 6))

# ── INTRO ────────────────────────────────────────────────────────────────────
story.append(Paragraph(
    "Tailscale crée un réseau privé entre nos machines. Une fois installé, "
    "tu accèdes au Z800 comme s'il était sur le même réseau local — depuis chez toi, "
    "depuis l'école, depuis n'importe où. Pas de port à ouvrir, pas de VPN compliqué.",
    s_body))
story.append(Spacer(1, 10))
story.append(HRFlowable(width="100%", thickness=1, color=BLEU_CLAIR))
story.append(Spacer(1, 10))

# ── ÉTAPES ───────────────────────────────────────────────────────────────────
story.append(Paragraph("Étapes d'installation", s_h1))
story.append(Spacer(1, 6))

# Étape 1
story.append(KeepTogether([
    step_block(1, "Créer un compte Tailscale (gratuit)", [
        Paragraph("Va sur <b>tailscale.com</b> et clique sur <i>Get started</i>.", s_step_body),
        Paragraph("Connecte-toi avec ton compte <b>Google</b> ou <b>GitHub</b> — c'est le plus rapide.", s_step_body),
        Paragraph(
            "⚠️  Utilise la même adresse email que celle que tu as donnée à Samir "
            "pour qu'il puisse t'envoyer l'invitation.", s_note),
    ]),
    Spacer(1, 8),
]))

# Étape 2
story.append(KeepTogether([
    step_block(2, "Installer Tailscale sur ta machine", [
        Paragraph("<b>Linux (Ubuntu/Debian) :</b>", s_step_body),
        code_block([
            "curl -fsSL https://tailscale.com/install.sh | sh",
            "sudo tailscale up",
        ]),
        Spacer(1, 6),
        Paragraph("<b>Windows :</b>", s_step_body),
        Paragraph(
            "Télécharge l'installateur sur <b>tailscale.com/download/windows</b>, "
            "lance le .exe, puis clique sur l'icône Tailscale dans la barre des tâches → <i>Log in</i>.",
            s_step_body),
        Spacer(1, 4),
        Paragraph("<b>macOS :</b>", s_step_body),
        code_block(["brew install tailscale", "sudo tailscale up"]),
        Paragraph("Ou installe depuis le Mac App Store (cherche \"Tailscale\").", s_note),
    ]),
    Spacer(1, 8),
]))

# Étape 3
story.append(KeepTogether([
    step_block(3, "Accepter l'invitation de Samir", [
        Paragraph(
            "Samir t'envoie une invitation par email (depuis Tailscale). "
            "Ouvre l'email et clique sur le lien pour accepter l'accès au serveur.",
            s_step_body),
        Paragraph(
            "Une fois accepté, le serveur Z800 (<b>ai</b>) apparaîtra dans ton interface Tailscale.",
            s_step_body),
    ]),
    Spacer(1, 8),
]))

# Étape 4
story.append(KeepTogether([
    step_block(4, "Vérifier que le serveur est visible", [
        Paragraph("Dans ton terminal, tape :", s_step_body),
        code_block(["tailscale status"]),
        Paragraph(
            "Tu dois voir une ligne avec <b>100.86.17.82</b> (le Z800). "
            "Si c'est le cas, tu es prêt !",
            s_step_body),
    ]),
    Spacer(1, 8),
]))

# Étape 5
story.append(KeepTogether([
    step_block(5, "Se connecter en SSH au Z800", [
        code_block(["ssh samir@100.86.17.82"]),
        Paragraph(
            "La première fois, il te demande de confirmer l'empreinte du serveur → tape <b>yes</b>.",
            s_step_body),
        Paragraph(
            "Si tu as une erreur <i>Permission denied</i>, envoie ta clé publique à Samir "
            "(voir section Dépannage ci-dessous).",
            s_note),
    ]),
]))

story.append(Spacer(1, 14))
story.append(HRFlowable(width="100%", thickness=1, color=BLEU_CLAIR))
story.append(Spacer(1, 10))

# ── COMMANDES UTILES ─────────────────────────────────────────────────────────
story.append(Paragraph("Commandes utiles", s_h1))
story.append(Spacer(1, 4))

cmd_data = [
    [Paragraph("Action", s_table_header), Paragraph("Commande", s_table_header)],
    [Paragraph("Connexion SSH", s_table_label),      Paragraph("ssh samir@100.86.17.82", s_table_cell)],
    [Paragraph("Copier un fichier vers Z800", s_table_label), Paragraph("scp fichier.py samir@100.86.17.82:/mnt/deep-learning/", s_table_cell)],
    [Paragraph("Récupérer un fichier du Z800", s_table_label),Paragraph("scp samir@100.86.17.82:/mnt/deep-learning/résultat.py .", s_table_cell)],
    [Paragraph("Statut Tailscale", s_table_label),   Paragraph("tailscale status", s_table_cell)],
    [Paragraph("Tunnel VNC (bureau distant)", s_table_label), Paragraph("ssh -L 5900:localhost:5900 samir@100.86.17.82", s_table_cell)],
]
cmd_table = Table(cmd_data, colWidths=[5*cm, 10.5*cm])
cmd_table.setStyle(TableStyle([
    ("BACKGROUND",    (0,0), (-1,0),  BLEU),
    ("BACKGROUND",    (0,1), (-1,1),  BLANC),
    ("BACKGROUND",    (0,2), (-1,2),  GRIS_CODE),
    ("BACKGROUND",    (0,3), (-1,3),  BLANC),
    ("BACKGROUND",    (0,4), (-1,4),  GRIS_CODE),
    ("BACKGROUND",    (0,5), (-1,5),  BLANC),
    ("VALIGN",        (0,0), (-1,-1), "MIDDLE"),
    ("LEFTPADDING",   (0,0), (-1,-1), 8),
    ("RIGHTPADDING",  (0,0), (-1,-1), 8),
    ("TOPPADDING",    (0,0), (-1,-1), 6),
    ("BOTTOMPADDING", (0,0), (-1,-1), 6),
    ("BOX",           (0,0), (-1,-1), 1, colors.HexColor("#CBD5E1")),
    ("INNERGRID",     (0,0), (-1,-1), 0.5, colors.HexColor("#E2E8F0")),
    ("ROUNDEDCORNERS",[4]),
]))
story.append(cmd_table)

story.append(Spacer(1, 14))
story.append(HRFlowable(width="100%", thickness=1, color=BLEU_CLAIR))
story.append(Spacer(1, 10))

# ── DÉPANNAGE ────────────────────────────────────────────────────────────────
story.append(Paragraph("Dépannage", s_h1))
story.append(Spacer(1, 4))

# Problème 1
story.append(Paragraph('<b>❌ "Permission denied (publickey)"</b>', s_body))
story.append(Paragraph("SSH utilise une clé cryptographique pour s'authentifier. "
    "Tu dois générer ta clé et l'envoyer à Samir :", s_body))
story.append(code_block([
    "# Générer ta clé (si tu n'en as pas)",
    "ssh-keygen -t ed25519 -C \"ton-email@gmail.com\"",
    "",
    "# Afficher ta clé publique (à envoyer à Samir)",
    "cat ~/.ssh/id_ed25519.pub",
]))
story.append(Paragraph(
    "Envoie le contenu affiché à Samir — il l'ajoutera sur le serveur.", s_note))
story.append(Spacer(1, 8))

# Problème 2
story.append(Paragraph('<b>❌ "connection timed out" ou "no route to host"</b>', s_body))
story.append(Paragraph("Vérifie que Tailscale tourne sur ta machine :", s_body))
story.append(code_block(["tailscale status    # doit afficher le Z800 (100.86.17.82)"]))
story.append(Paragraph(
    "Si le Z800 n'apparaît pas, vérifie que tu as bien accepté l'invitation de Samir.", s_note))
story.append(Spacer(1, 8))

# Problème 3
story.append(Paragraph('<b>❌ Tailscale bloqué au lycée / à l\'école</b>', s_body))
story.append(Paragraph(
    "Tailscale bascule automatiquement sur HTTPS (port 443) si UDP est bloqué. "
    "Dans 95% des cas ça fonctionne quand même. Si ça ne passe pas, "
    "utilise ton téléphone en partage de connexion.", s_body))

story.append(Spacer(1, 14))
story.append(HRFlowable(width="100%", thickness=1, color=BLEU_CLAIR))
story.append(Spacer(1, 10))

# ── CONTACT ──────────────────────────────────────────────────────────────────
contact = Table([[
    Paragraph(
        "<b>Un problème ?</b> Contacte Samir :\n"
        "hamouda.samir23@gmail.com",
        ParagraphStyle("contact", fontSize=10, leading=15,
            textColor=colors.HexColor("#1E40AF"),
            fontName="Helvetica", alignment=TA_CENTER)
    )
]], colWidths=[15.5*cm])
contact.setStyle(TableStyle([
    ("BACKGROUND",    (0,0), (-1,-1), BLEU_CLAIR),
    ("ROUNDEDCORNERS",[8]),
    ("LEFTPADDING",   (0,0), (-1,-1), 20),
    ("RIGHTPADDING",  (0,0), (-1,-1), 20),
    ("TOPPADDING",    (0,0), (-1,-1), 12),
    ("BOTTOMPADDING", (0,0), (-1,-1), 12),
]))
story.append(contact)
story.append(Spacer(1, 8))

story.append(Paragraph(
    "Documentation complète : github.com/hamouda23/ubuntu-server-network-rtl8192eu",
    ParagraphStyle("footer", fontSize=8, textColor=colors.HexColor("#9CA3AF"),
        fontName="Helvetica", alignment=TA_CENTER)
))

# ── BUILD ────────────────────────────────────────────────────────────────────
doc.build(story)
print(f"PDF généré : {OUTPUT}")
