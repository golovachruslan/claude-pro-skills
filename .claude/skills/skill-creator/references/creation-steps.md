# Skill Creation Steps (Detailed)

## Step 1: Understanding the Skill with Concrete Examples

Skip this step only when the skill's usage patterns are already clearly understood.

To create an effective skill, clearly understand concrete examples of how the skill will be used. This understanding can come from either direct user examples or generated examples that are validated with user feedback.

For example, when building an image-editor skill, relevant questions include:

- "What functionality should the image-editor skill support? Editing, rotating, anything else?"
- "Can you give some examples of how this skill would be used?"
- "I can imagine users asking for things like 'Remove the red-eye from this image' or 'Rotate this image'. Are there other ways you imagine this skill being used?"
- "What would a user say that should trigger this skill?"

To avoid overwhelming users, avoid asking too many questions in a single message.

## Step 2: Planning the Reusable Skill Contents

Analyze each example by:

1. Considering how to execute on the example from scratch
2. Identifying what scripts, references, and assets would be helpful when executing these workflows repeatedly

**Example - pdf-editor skill**: Rotating a PDF requires re-writing the same code each time → a `scripts/rotate_pdf.py` script would be helpful.

**Example - frontend-webapp-builder skill**: Writing a frontend webapp requires the same boilerplate each time → an `assets/hello-world/` template would be helpful.

**Example - big-query skill**: Querying BigQuery requires re-discovering table schemas each time → a `references/schema.md` file would be helpful.

## Step 3: Initializing the Skill

When creating a new skill from scratch, always run the `init_skill.py` script:

```bash
scripts/init_skill.py <skill-name> --path <output-directory>
```

The script creates the skill directory with a SKILL.md template, and example `scripts/`, `references/`, and `assets/` directories.

Skip this step if the skill already exists and iteration or packaging is needed.

## Step 4: Edit the Skill

Remember that the skill is being created for another instance of Claude to use. Include information that would be beneficial and non-obvious.

### Learn Proven Design Patterns

Consult these guides based on your skill's needs:
- **Multi-step processes**: See references/workflows.md
- **Specific output formats**: See references/output-patterns.md

### Start with Reusable Skill Contents

Begin with the reusable resources identified in Step 2. Note that this step may require user input (e.g., brand assets, documentation).

Added scripts must be tested by running them. Delete any example files not needed for the skill.

### Update SKILL.md

**Writing Guidelines:** Always use imperative/infinitive form.

**Frontmatter**: Write `name` and `description`. Description is the primary triggering mechanism — include both what the skill does and specific triggers/contexts. Include all "when to use" information in the description, not the body.

**Body**: Write instructions for using the skill and its bundled resources.

## Step 5: Packaging a Skill

Package into a distributable .skill file:

```bash
scripts/package_skill.py <path/to/skill-folder>
```

Optional output directory: `scripts/package_skill.py <path/to/skill-folder> ./dist`

The script validates (frontmatter, naming, description, structure) then packages. Fix any validation errors and re-run if it fails.

## Step 6: Iterate

After testing, users may request improvements. Iteration workflow:

1. Use the skill on real tasks
2. Notice struggles or inefficiencies
3. Identify how SKILL.md or bundled resources should be updated
4. Implement changes and test again
