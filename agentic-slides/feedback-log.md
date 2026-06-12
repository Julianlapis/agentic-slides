---
name: feedback-log
description: Agentic Slides Feedback Log - read at the start of every /agentic-slides invocation to avoid repeating mistakes
---

# /agentic-slides Feedback Log

Read this file at the start of every `/agentic-slides` invocation. Entries here are binding corrections from previous sessions — they override default skill behavior.

At the end of every session, append any new corrections the user made. Format:

```
<!-- id: YYYY-MM-DD-short-slug -->
## What was corrected
One or two sentences describing the mistake and the binding rule that replaces it.
```

## 25-Entry Gate

If active entries (lines matching `<!-- id:`) exceed 25, warn the user that the log should be consolidated — older entries that have become permanent behavior belong in the reference files, not here.

---

*(No entries yet. The log grows as you use the skill.)*
