# BUILD_LOG.md

## Task 1 -- Scaffold repo and write CLAUDE.md
- Brief: Create the repo structure and write CLAUDE.md with stack, data shape, conventions, and out-of-scope list.
- What Claude proposed: Standard Flask scaffold with SQLAlchemy and a database migration.
- What I changed before approving: Told it no database -- in-memory only. Rewrote CLAUDE.md myself to lock that in.
- Verification: `python app.py` started without errors. CLAUDE.md present at root.
- One thing I learned: Writing CLAUDE.md first saved me from Claude reaching for a database on every subsequent task.

## Task 2 -- Define in-memory data structure
- Brief: A session is a dict with subject, duration_minutes, mood, and date. All sessions live in a list in app.py.
- What Claude proposed: A Session dataclass with validation methods baked in.
- What I changed before approving: Plain dict only -- no dataclass, no class at all. Kept it consistent with the sandbox pattern.
- Verification: Added a session manually in a Python shell, printed the list, confirmed the shape.
- One thing I learned: Claude defaults to the more "correct" pattern even when simple is better. You have to explicitly say simple.

## Task 3 -- Write add_session() helper
- Brief: A function in helpers.py that validates subject, duration, and mood then appends a session dict to the list.
- What Claude proposed: The function plus a separate validation module.
- What I changed before approving: No separate module -- validation stays inside add_session(). One file, one function.
- Verification: `pytest tests/test_helpers.py -q` -- all add_session tests green.
- One thing I learned: Claude likes to split things into more files than you need. Push back early or it compounds.

## Task 4 -- Build POST route /add
- Brief: Read subject, duration_minutes, mood from form data, call add_session(), redirect to /.
- What Claude proposed: The route plus a duplicate validation block inside the route itself.
- What I changed before approving: Removed the duplicate validation -- add_session() already handles it. Route just catches the ValueError and passes it to the template.
- Verification: Submitted the form manually, confirmed the session appeared on the home page.
- One thing I learned: Claude doesn't always trust the helpers it just wrote. Point it back at them.

## Task 5 -- Build the add-session form
- Brief: templates/add.html with fields for subject, duration, and mood dropdown. Shows error message if one is returned.
- What Claude proposed: The form plus JavaScript client-side validation.
- What I changed before approving: No JavaScript -- server-side only. Removed the script block entirely.
- Verification: Loaded /add in browser, submitted empty subject, confirmed error message appeared.
- One thing I learned: Claude adds JS validation by default because it looks professional. It's out of scope until you say so.

## Task 6 -- Build home route /
- Brief: Pass all sessions and the weekly summary and streak count to index.html.
- What Claude proposed: Correct -- no pushback needed. Single route, three template variables.
- What I changed before approving: Nothing. Approved as proposed.
- Verification: `GET /` returned 200. Sessions added via /add appeared in the template.
- One thing I learned: When the brief is tight enough, Claude gets it right on the first try.

## Task 7 -- Write weekly_summary() helper
- Brief: Group sessions from the current Mon-Sun week by subject, sum duration_minutes per subject, return a dict.
- What Claude proposed: The helper plus a separate date utility module.
- What I changed before approving: No separate module -- date logic stays inside the function. Three extra lines is not a module.
- Verification: Unit test with known fixture data returned correct totals. `pytest -q` green.
- One thing I learned: The weekly boundary (Monday, not 7 days ago) matters and Claude got it right -- but I verified it with a test anyway.

## Task 8 -- Render weekly summary as bar chart
- Brief: Inline CSS bars in index.html, width proportional to hours, no JS library.
- What Claude proposed: A Chart.js implementation with a canvas element.
- What I changed before approving: No Chart.js -- CSS bars only. Removed the script tag and rewrote the template section.
- Verification: Loaded the page with two subjects logged, confirmed bars rendered with different widths.
- One thing I learned: Claude always reaches for a library when CSS will do. Name the constraint explicitly or it won't hold.

## Task 9 -- Write streak_count() helper
- Brief: Count consecutive days ending today where at least one session was logged. Return 0 if none today.
- What Claude proposed: Correct implementation. No pushback needed.
- What I changed before approving: Nothing -- read it carefully, it was right.
- Verification: Unit tests covering today-only, three consecutive days, and a gap. All green.
- One thing I learned: I couldn't verify the date arithmetic by reading it cold -- I needed the tests to trust it. That's a knowledge gap to close.

## Task 10 -- Display streak on home page
- Brief: Show streak count in index.html next to the weekly summary. Singular/plural handled.
- What Claude proposed: Correct. One template change, no logic added to the route.
- What I changed before approving: Nothing.
- Verification: Loaded page, confirmed "1 day" vs "3 days" rendered correctly.
- One thing I learned: Small tasks with tight briefs take five minutes. The decomposition is the work.

## Task 11 -- Write full test suite
- Brief: Tests for add_session(), weekly_summary(), and streak_count() covering edge cases.
- What Claude proposed: Tests plus a conftest.py with shared fixtures.
- What I changed before approving: No conftest -- tests are simple enough to be self-contained. Removed it.
- Verification: `pytest -q` -- 8 passed, 0 failed.
- One thing I learned: Claude writes conftest.py reflexively on any multi-function test file. It's not always needed.

## Task 12 -- Polish UI and empty states
- Brief: Show "No sessions yet" when list is empty. Consistent spacing. No new features.
- What Claude proposed: Empty state plus a loading spinner for future async use.
- What I changed before approving: No spinner -- nothing async exists. Removed it.
- Verification: Loaded app with empty sessions list, confirmed message appeared instead of blank page.
- One thing I learned: Claude anticipates future features and adds hooks for them. That's scope creep even when it's well-intentioned.

## AI Workflow

**Planning:** Claude.ai chat handled all design decisions -- data shape, route
structure, edge cases, scope cuts. No code, just thinking. Kept the repo clean
while the plan was still changing.

**Executing:** Claude Code with plan mode for every task. Pasted the brief,
read the plan, pushed back when it overreached, then approved. One task at a
time.

**Polishing:** Claude Code for small cleanup -- empty state messaging, error
display on the form. Tight briefs, single-file scope.

**Reviewing:** Read every diff myself before committing. Ran pytest manually
rather than trusting Claude's "tests pass" output.

**Where chat outperformed Code:** Scoping the feature. Claude Code would have
started building immediately. Chat let me push back on scope before a single
file was touched.

**Where I switched mid-task:** Started a UI polish task in Claude Code, realized
I hadn't decided what the empty state should say. Switched to chat to think it
through, then came back to Code with a clear answer.

## Reflection

**Where the agentic workflow let me ship things I couldn't have alone:**
The bar chart and streak logic would have taken me hours to figure out
independently. I know what I want a feature to do but translating that into
working Flask routes and Jinja templates from scratch is slow when you're
still building fluency. Claude handled the mechanical translation fast, which
meant I could spend my time on the decisions that actually required judgment --
what the feature should do, what's out of scope, what the data shape should
look like. The whole app in roughly four hours would not have happened without
that speed.

**Where I had to step in and override Claude:**
Twice it tried to combine tasks I had deliberately kept separate. When I asked
for the weekly summary logic it also started drafting the template changes,
because from Claude's perspective those are naturally connected. I had to stop
it and say do the helper function only. It also defaulted to more complex data
structures than I needed -- wanted to add a separate subject registry when a
plain dict key was fine.

**What this project revealed about my own judgment and knowledge gaps:**
The honest answer is that I'm better at knowing what I want than I am at
knowing whether what Claude gave me is correct. I could read the plan and say
"that's too much" or "that's the wrong file." But when Claude wrote the streak
logic I couldn't verify it by reading it cold -- I had to run it against test
cases to trust it. That's a gap. A more experienced developer would read that
function and immediately see whether the date arithmetic was right. I had to
let the tests tell me.

The thing this cohort surfaced that I didn't expect: the bottleneck isn't
getting Claude to produce code. The bottleneck is having enough knowledge to
evaluate what it produces. I could identify all four bugs in the bug hunt once
they were pointed out. But would I have caught them in a real review, under
time pressure? I'm not sure. That uncertainty is useful to name.

I also noticed I'm much better at decomposition than I expected. Breaking the
feature into ordered tasks with verification steps felt natural. That might be
the most transferable skill from this whole cohort -- not the Claude prompting,
but the habit of asking "what's the smallest next thing and how will I know it
worked."

**How I'll bring this into my internship:**
First thing on day one: read the codebase before I open Claude Code. Understand
the stack, the conventions, the data shape. The context engineering lesson
applies whether or not I'm literally writing a brief -- know the constraints
before you ask for anything.

The workflow I'll default to: chat for design questions, Code for
implementation, plan mode before every non-trivial task, and I verify the
output myself before I call it done. I won't trust "tests pass" in Claude's
output. I'll run them.

The thing I'll tell myself every day: Claude is fast and I am the judge. If I
can't evaluate what it produced, that's a signal I need to understand the
problem better before I ask for help with it.