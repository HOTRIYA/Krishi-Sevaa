import sys

with open('c:/Users/Hp/Downloads/Krishi-Seva-main (1)/Krishi-Seva-main/KisanSeva_unified.jsx', 'r', encoding='utf-8') as f:
    text = f.read()

# Replace App signIn/signOut and state
text = text.replace(
    'const [authed, setAuthed] = useState(false);',
    'const [authed, setAuthed] = useState(false);\n  const [loggedInRole, setLoggedInRole] = useState(null);'
)

text = text.replace(
    'const signIn = (role) => { setAuthed(true); setPublicMode(false); setActiveRole(role); };',
    'const signIn = (role) => { setAuthed(true); setPublicMode(false); setActiveRole(role); setLoggedInRole(role); };'
)

text = text.replace(
    'const signOut = () => { setAuthed(false); setActiveRole("authority"); setPublicMode(true); setMobileGate(null); };',
    'const signOut = () => { setAuthed(false); setActiveRole("authority"); setLoggedInRole(null); setPublicMode(true); setMobileGate(null); };'
)

text = text.replace(
    '<RoleSwitcherBar activeRole={activeRole} setActiveRole={setActiveRole} onSignOut={signOut} darkMode={darkMode} setDarkMode={setDarkMode} />',
    '<RoleSwitcherBar activeRole={activeRole} setActiveRole={setActiveRole} loggedInRole={loggedInRole} onSignOut={signOut} darkMode={darkMode} setDarkMode={setDarkMode} />'
)

# Replace RoleSwitcherBar signature and check
text = text.replace(
    'function RoleSwitcherBar({ activeRole, setActiveRole, onSignOut, darkMode, setDarkMode }) {',
    'function RoleSwitcherBar({ activeRole, setActiveRole, loggedInRole, onSignOut, darkMode, setDarkMode }) {'
)
text = text.replace(
    'if (activeRole !== "admin") {',
    'if (loggedInRole !== "admin") {'
)

with open('c:/Users/Hp/Downloads/Krishi-Seva-main (1)/Krishi-Seva-main/KisanSeva_unified.jsx', 'w', encoding='utf-8') as f:
    f.write(text)

print("Fixed RoleSwitcherBar logic")
