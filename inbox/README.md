# Inbox

Drop anything new and unprocessed here: an Overleaf zip, the PDF of a thesis or article, a template, images, notes.
Then tell Claude "process the inbox" (Slovak: *spracuj inbox*).

What happens to the content:

| Type | Destination |
|---|---|
| zip with a LaTeX project | unpacked to `projects/<project>/`, zip to `archives/` |
| zip with a template | unpacked to `templates/<template>/`, zip to `archives/` |
| PDF of the author's own work or of a professional source | `knowledge/sources/` + extracted text + overview in `knowledge/research/` |
| bibliography (`.bib`) | verified entries into `knowledge/bibliography/references.bib` |
| anything else | by content; what cannot be filed stays here and Claude asks |

After processing, this folder must be empty (except this file).
