# DrivePulse: Final Prototype Notes

## Changes you asked for
- **Colour restored.** Removed the greyscale filter. Palette: indigo (main actions), green (verified / progress), amber (saved / medium), red (hard).
- **Active page is shown.** The current page is highlighted in the sidebar (desktop) and the top bar (mobile) and marked with `aria-current="page"`.
- **Hover effects are back** on links, cards and buttons (they were removed only for the earlier rough prototype).

## Bugs fixed

### Data / database (`db.js`)
1. **Old saved data could break new code.** Storage key changed to `drivepulse_db_v2`; bump it whenever the seed data shape changes.
2. **Blocked or private-mode storage crashed saving.** Storage is now tested on load. If blocked, a yellow banner explains that changes won't be saved instead of failing silently.
3. **Generic element IDs (`a`, `b`, `c`, `d`, `q`, `f`, `m`, `p`) used as global variables.** Replaced with descriptive IDs and a `$()` helper to avoid name clashes.

### Debriefs page
4. **Cards jumped around after upvoting.** Sorting now ignores your own vote, so the list stays still.
5. **Your new post was hidden at the bottom** (unverified posts sort last). After posting you are now taken straight to your debrief (`debriefs.html?q=Company`), and it carries a "your post" label.
6. **Search only matched company and role.** It now also searches the tip and all three rounds.
7. **Upvote and save buttons had no accessible state.** Added `aria-pressed`; Save now turns amber when saved.
8. **Text typed by users was rendered as HTML.** All user text is escaped (tested with `<b>` input).

### Post page
9. **Same company typed in different case** (e.g. "sandhu infotech") created a mismatch, so counts were wrong. It now matches the existing company name ignoring case.
10. **A brand-new company never appeared on the Companies page.** New companies are now added automatically with placeholder details.
11. **Spaces-only answers passed validation.** Input is trimmed and rejected with a red message if empty.
12. **Double submit created duplicate posts.** The button is disabled after submitting.
13. **Offer letter did nothing.** The file name is stored, the message says it is queued, and the badge stays "Pending" (real verification is not built).
14. **Form fields had only placeholders.** Added `aria-label`s.

### Other pages
15. **Companies "Prep" link did not open that company's pathway.** It now opens `pathways.html?c=Company`, and is hidden for companies with no pathway yet.
16. **Pathway progress used a fixed `/7`.** Uses the real number of tasks, so changing a pathway's length won't break it.
17. **Profile progress used a hard-coded total.** Now calculated from all pathways.
18. **Mobile nav scrolled away.** It is now sticky.
19. **Missing favicon caused a 404 in the console.** Added an inline icon.

## Tested (automated smoke test)
All 6 pages load without JavaScript errors; upvote, save, posting a debrief (with a messy company name and HTML in the tip), company merge, Companies, Profile stats and the `?c=` pathway link all behave correctly. This ran in a simulated browser, so **please click through it once in a real browser to check the look**.

## Known limits (by design, for a prototype)
- Data lives in each browser's `localStorage`: it is not shared between users or devices. Use Profile > "Export db.json" to save it, "Reset demo data" to start over.
- Offer-letter verification, login and admin approval are not built.
- Tailwind is loaded from its CDN (needs internet). For production, build Tailwind properly.
- All companies, names and debriefs are made-up dummy data.

## Files
`index.html`, `debriefs.html`, `pathways.html`, `post.html`, `companies.html`, `profile.html`, `db.js` (keep together in one folder; open `index.html`).
