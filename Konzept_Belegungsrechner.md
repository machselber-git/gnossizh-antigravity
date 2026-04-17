# Konzept: gnossiZH Belegungs-Rechner

Dieses Tool dient als "Hook", um Nutzer:innen auf die Website zu ziehen und ihre E-Mail-Adresse für den Newsletter zu gewinnen.

## 1. Nutzerführung (UX Flow)
1. **Landing:** "Finde heraus, welche Wohnungsgrösse du in Zürich wirklich bekommst."
2. **Input:** Zwei einfache Regler oder Plus/Minus-Buttons:
   - "Wie viele Erwachsene ziehen ein?"
   - "Wie viele Kinder ziehen ein?"
3. **Dynamic Result:** Sofortige Anzeige der Zimmeranzahl (z.B. "3.5 bis 4.5 Zimmer").
4. **Lead Magnet:** "Willst du benachrichtigt werden, sobald eine passende Wohnung frei wird? [E-Mail Eingabe]"

## 2. Die Logik (Basierend auf Zürcher Statuten)
Die Standard-Regel der meisten Genossenschaften (ABZ, FGZ, BEP) ist:
**Personenanzahl + 1 = Maximale Zimmeranzahl**

*Beispiele:*
- 1 Person (Single) -> 1 bis 2.5 Zimmer (oft max. 2.0 gefordert).
- 2 Personen (Paar) -> 2 bis 3.5 Zimmer.
- 3 Personen (Paar + 1 Kind) -> 3 bis 4.5 Zimmer.
- 4 Personen (Paar + 2 Kinder) -> 4 bis 5.5 Zimmer.

*Sonderregeln (optional einbaubar):*
- **Stiftungen:** Oft strenger (Personen = Zimmer).
- **WG-Modus:** Rechner fragt, ob es eine WG ist (Zimmer = Personen).

## 3. Strategie gegen das "Abmelde-Problem" (The Success Loop)
Um das Problem zu lösen, dass erfolgreiche Nutzer:innen einfach verschwinden:

### A. Der "Lotto-Check" (Off-Boarding Umfrage)
Wenn jemand auf "Abmelden" klickt, erscheint eine einseitige, emotionale Frage:
> "Oh, gehst du schon? Hast du über gnossiZH eine Wohnung gefunden? 😍"
> - [ ] Ja, dank euch!
> - [ ] Ja, woanders.
> - [ ] Nein, ich gebe auf.

### B. Das "Success-Incentive"
Wer "Ja, dank euch!" klickt, kriegt ein Angebot:
> "Hammer! Teile deine Story (nur 2 Sätze) und wir schicken dir ein 'Starthilfe-Paket' (z.B. einen 20 CHF Gutschein für einen lokalen Zürcher Partner wie die Stadtgärtnerei oder ein Café)."
> *Dieses 'Gold' (die Story) ist für dein Marketing 100x mehr wert als die 20 CHF.*

### C. Referral-Link in der "Glückwunsch-Mail"
In der Mail, in der die Nutzer:innen sagen "Ich ziehe aus", fragen wir aktiv:
> "Kennst du jemanden, der noch sucht? Schick ihnen gnossiZH als Abschiedsgeschenk."

---
## Nächste Schritte
1. **Frontend-Prototyp:** Erstellung einer einfachen HTML/CSS-Version des Rechners.
2. **Newsletter-Integration:** Formular so verknüpfen, dass die gewählte Zimmergrösse direkt als Tag gespeichert wird.
