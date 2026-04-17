from colorama import init, Fore, Back, Style

init(autoreset=True)

# ── Raccourcis couleurs ───────────────────────────────────
VERT       = Fore.GREEN + Style.BRIGHT
ROUGE      = Fore.RED + Style.BRIGHT
JAUNE      = Fore.YELLOW + Style.BRIGHT
CYAN       = Fore.CYAN + Style.BRIGHT
BLANC      = Fore.WHITE + Style.BRIGHT
MAGENTA    = Fore.MAGENTA + Style.BRIGHT
BLEU       = Fore.BLUE + Style.BRIGHT
RESET      = Style.RESET_ALL
GRIS       = Fore.WHITE + Style.DIM


def ok(msg):
    print(f"{VERT}✅ {msg}{RESET}")

def erreur(msg):
    print(f"{ROUGE}❌ {msg}{RESET}")

def warning(msg):
    print(f"{JAUNE}⚠️  {msg}{RESET}")

def info(msg):
    print(f"{CYAN}ℹ️  {msg}{RESET}")

def titre(msg):
    print(f"\n{CYAN}{'─' * 45}{RESET}")
    print(f"{BLANC}  {msg}{RESET}")
    print(f"{CYAN}{'─' * 45}{RESET}")

def section(msg):
    print(f"\n{MAGENTA}  ── {msg} ──{RESET}")
