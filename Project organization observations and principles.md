# Project organization observations and principles

Ad hoc working reference, 28 October 2026. For Hunter and assistants working across `C:\apps`, with `astToolFactory` as the immediate focus.

The recurring practice is to make meaning, authority, and responsibility part of the structure of the work. An identifier, type, module, filename, or configuration boundary can carry information that would otherwise require additional explanation or computation. The same principles recur within a function, across modules, between subsystems, and across repositories.

This reference collects observations, Hunter's stated principles, concrete examples, and places where the material could become more permanent. **Principle** identifies a normative statement grounded in Hunter's clarifications or the linked current guidance. **Observation** describes the surveyed code. Suggested documentation destinations remain proposals.

## Authority and scope

**Principle.** Look for rules that remain useful at different scales. Identify both the hierarchy of authority and the scope over which each authority applies.

Hunter describes two directions. In the vertical direction, an authority can inherit or specialize another authority. In the horizontal direction, the resulting rule applies across the members of its scope.

The configuration files provide a concrete example. The common root `ruff.toml` extends the repository's `pyproject.toml`. In `mapFolding`, the tests' `ruff.toml` extends that root configuration and changes the line length; research and archive configurations make their own scoped adjustments. Each resulting configuration affects the files within its applicable scope. The hierarchy permits a shared baseline and narrower policies.

The same pattern occurs in code. `mapFolding.theSSOT` supplies package settings; `mapFolding.kitAST.theSSOT` supplies generator settings and specializes copied base defaults for different algorithm families. Each settings object supplies decisions to multiple consumers.

**Observation.** SSOT recurs at package and subsystem scope. Its contents include settings classes, instances, derived paths, identifier mappings, and selected defaults. The relevant authority depends on the particular decision being made.

References: [shared Ruff configuration](C:/apps/hunterMakesPy/ruff.toml), [test specialization](C:/apps/mapFolding/mapFolding/tests/ruff.toml), [research specialization](C:/apps/mapFolding/Z0Z_research/ruff.toml), [package settings](C:/apps/mapFolding/mapFolding/theSSOT.py), and [generator defaults](C:/apps/mapFolding/mapFolding/kitAST/theSSOT.py).

## Meaning and representation

**Principle.** Add meaning when the code does not let the reader identify what a value represents or distinguish the things being tracked.

The practical trigger is a block of code in which the meaning of a float is unclear, or two dictionaries could plausibly be tracking the same things. The design must expose the relevant distinction or shared identity. A Python storage class alone does not answer that question.

`Leaf` acquired an alias because many of the integers represented leaves and that identity mattered. The motivation was the represented concept and its recurrence. Introducing aliases for arbitrary integers would not reproduce that decision.

For a mapping, identify what the keys denote, what the values denote, and what relation the mapping expresses. When two objects represent the same concept, retain that identity through calls and attributes. When they represent different concepts, express the actual difference. These decisions can affect types, identifiers, records, and ownership together.

**Observation.** Semiotics supplies runtime vocabulary such as `inclusive`, `decreasing`, `zeroIndexed`, `noMinimum`, leaf and pile origins, and positional coordinate symbols. Type definitions express domain roles, relationships, storage, and shape. Both contribute meaning; their immediate uses differ.

The existing identifier guidance states this directly: equal numbers or equal Python types do not establish equal meaning. Its semantic constants also have specific meanings. `inclusive` expresses boundary inclusion; it is not a replacement for an ordinary increment merely because its value is one.

Permanent references: [Python identifiers](C:/Users/hunte/.codex/skills/python-identifiers/SKILL.md), [identifier standards](C:/Users/hunte/.codex/skills/python-identifiers/references/identifier-standards.md), and [type annotation guidance](C:/Users/hunte/.codex/skills/python-code-generation/references/type-annotations.md). Domain examples: [mapFolding types](C:/apps/mapFolding/mapFolding/theTypes.py), [coordinate notation](C:/apps/mapFolding/mapFolding/_semiotics.md), and [symbol reference](C:/apps/mapFolding/mapFolding/_symbols.md).

## Structure that performs useful work

**Principle.** Choose a structure whose existing operations carry the required meaning and perform the required work. Preserve the work that this arrangement eliminates when evaluating or changing the design.

Hunter traces this practice to batch scripts, where variable and file names regularly encode useful information. Python's lack of a general way for a variable to know its own name motivates putting information in names and structures that the program can actually consume. These examples go beyond making labels descriptive.

### Selector records in astToolFactory

The selector system makes the relationship between names and values available to the executor. For example, this existing assignment specifies both selection and action:

```python
Column__ClassDefIdentifier_attribute('FunctionDef', 'args'): column__value('attributeRename', 'argumentSpecification')
```

The selector's class identifier encodes the relevant columns. Its `NamedTuple` fields are the actual column identifiers, and its values are the values to match. The assignment record supplies the destination column and its value. The current executor obtains the selector's field/value associations through `_asdict()` and combines the column comparisons. It consumes `assign.column` and `assign.value` to perform the assignment.

The class naming convention, record schema, and executor therefore work together. The programmer supplies a compact specification whose structure already associates each value with its meaning. The executor does not need a separate case for each selector class. Adding another selector shape can use the same field-driven mechanism.

This is also why the selector classes are required at runtime: they construct the specifications consumed by the program. Describing them only as annotation types or elaborate names misses their operational role.

References: [selector classes](C:/apps/astToolFactory/astToolFactory/_theTypes.py), [assignment specifications](C:/apps/astToolFactory/astToolFactory/datacenter/_dataframeUpdateAnnex.py), and [selection and assignment executors](C:/apps/astToolFactory/astToolFactory/datacenter/_dataframeUpdate.py:842).

### Filenames as keys and appended contributions as sums

Hunter's account describes using disk storage in place of retaining contributions in memory. A file is named for its `arcCode`; each contribution to its meanders value is appended. After writing finishes, the filename supplies the key and the contents supply contributions to sum. The number of contributions is irrelevant to the result.

The structure performs several jobs:

- The filename carries the identity that will become a dictionary key or dataframe value.
- Selecting that filename places a contribution in its group as it is written.
- Appending records a contribution without reading and rewriting an accumulated total.
- Reading all contributions and summing them handles their variable number directly.
- The reader does not need to count contributions or infer which key a payload belongs to.

The writing and reading already have to happen. Their arrangement supplies grouping and identity without another layer of interpretation. Ordinary conversion of a filename's text to an integer preserves the key; it does not require reconstructing the mathematical meaning of the encoded state.

The archived implementation located for this example is [A005316write2disk.py](C:/apps/mapFolding/archive/matrixMeanders/A005316write2disk.py:70). It uses the older names `curveLocationAnalysis` and `distinctCrossings`. The writer names the file with the state value and appends each contribution followed by `+`; the reader converts the filename stem to an integer key and evaluates the stored addition expression. Hunter's line-based recollection and this archived variant use different encodings of the contributions, while illustrating the same arrangement of identity, grouping, append, and reduction.

The example establishes a design principle. The archived threading and expression-evaluation implementation is not a current implementation prescription. Completion of writing is part of the producer/consumer contract described by Hunter and the reader's own docstring.

### Contracts and unnecessary work

**Principle.** Do not introduce interpretation, counting, validation, or bookkeeping for information that the structure and established producer contract already provide. Select operations that handle the valid input's natural variation, such as a sum over any number of contributions.

This principle connects to the current [post-defensive computation guidance](C:/Users/hunte/.codex/skills/python-code-generation/references/post-defensive.md): determine reliability from the producer's actual contract, perform necessary verification at meaningful ingress, and let downstream computation use the established guarantees. The disk example's irrelevant row count supplies no new fact needed to calculate the sum.

## Imports reflect how an object is used

**Principle.** Keep annotation-only dependencies in `TYPE_CHECKING` blocks where appropriate. Import values and constructors normally when execution needs them.

**Observation.** Types tend to appear in type-checking blocks, while semiotic values enter ordinary computation. A module named `_theTypes` can also contain runtime constructors, and a type definition can select concrete storage. Import placement follows the use of the particular object.

The selector records are a substantive runtime example. `mapFolding` also uses some type definitions to select NumPy storage. Their presence outside a type-checking block does not erase the distinction between annotation dependencies and runtime dependencies.

Reference: [type annotation guidance](C:/Users/hunte/.codex/skills/python-code-generation/references/type-annotations.md).

## Responsibility and recurring homes

**Observation.** The projects repeatedly give these responsibilities recognizable homes, with variation in names and granularity:

| Responsibility                              | Recurring homes                                                           |
| ------------------------------------------- | ------------------------------------------------------------------------- |
| Shared settings and authoritative decisions | `theSSOT`, `_theSSOT`, settings objects, base and specialized defaults    |
| Domain meaning and notation                 | semiotics modules, meaningful identifiers, symbol guides, editor snippets |
| Type relationships and structured records   | `theTypes`, `_theTypes`, more local record definitions                    |
| Working state and storage construction      | `dataBaskets`, `dataStructures`                                           |
| Reused operations                           | `beDRY`, `kitAST`, `kitFilesystem`, shared utility packages               |
| Main operations and coordination            | factories, generators, algorithm modules, `doTheNeedful`, runners         |
| Material consumed by those operations       | annexes, snippets, policy dictionaries, documentation material            |
| Intentional import surfaces                 | explicit package re-exports                                               |
| Test material and support                   | `dataSamples`, `conftest.py`, `conftestAnnex.py`                          |
| Work at different stages                    | research, development, notes, archives, synthesized output                |

**Principle.** Determine responsibility from the knowledge, decisions, and effects an operation requires. A familiar filename or similar signature is evidence to investigate, not sufficient proof of ownership.

**Principle.** Domain boundaries are strict. The datacenter and the factory are separate domains, and their operations belong in separate modules. All dataframe changes occur in `datacenter/_dataframeUpdate.py`. Its annex stores specifications of potential changes; it does not apply them. The factory owns code synthesis. A shared upstream source does not establish a shared domain: `typeshed` identifies a source, not a domain, and does not justify combining datacenter operations with factory operations in one module.

The current [design coherence guidance](C:/Users/hunte/.codex/skills/python-identifiers/references/design-coherence.md) explains that analysis. It also distinguishes placement from generality: an operation can belong to a local scope because it implements that scope's particular policy.

**Principle.** When a concept or function can be generalized to its fullest extent, `hunterMakesPy` is its usual home. Packages consume that general definition from `hunterMakesPy`. For example, `hunterMakesPy` defines and exports `identifierDotAttribute: TypeAlias = str`; `astToolkit` and `astToolFactory` import that definition from `hunterMakesPy`.

Recent changes include both extraction and consolidation. In the surveyed working tree, `astToolFactory/filesystem.py` gathers dataframe persistence and generated-module writing, while `_storage.py` is removed. The Ingredients abstractions have been removed from `astToolkit` and their use removed from `astToolFactory`; they now reside in `mapFolding.kitAST`. `mapFolding` has also consolidated semiotics and shared helpers. These changes do not establish a rule that more modules or more abstractions are inherently desirable.

Source and generation responsibilities also remain distinguishable. `astToolFactory` manufactures tools in the sibling `astToolkit` project. `mapFolding` separates source algorithms, transformation machinery, and synthesized variants. Repeated generated text can have one authoritative producer.

**Reorganization goal.** A substantial portion of `astToolkit` is synthesized by `astToolFactory`, and the reorganization aims to increase that portion while respecting domain boundaries and the reliability of each transformation. Typeshed's `ast.pyi`, for example, supplies the constant-value union used to synthesize `ast_ConstantValue` in `astToolkit.theTypes`. The location TypedDicts retain their handmade definitions.

## Common policy across repositories

**Principle.** Maintain uniform development rules across repositories, with explicit specialization where a narrower scope requires it.

**Observation.** The root configuration files are local attachment points for common policy. `hunterMakesPy` supplies the shared files used by [makeSymlinks.cmd](C:/apps/Z0Z_/makeSymlinks.cmd). The sampled configurations are Windows hard links and are tracked by Git as ordinary files. Several repository paths can therefore share one local file while each repository records its contents.

The mechanism includes hard links for shared configurations, directory symlinks for shared typing material from `stubFileNotFound`, and copied starter files. These mechanisms have different behavior. The current configuration-link script creates missing paths and leaves existing paths alone, without reconciling whether an existing file still shares the intended identity. Hunter reports that synchronization repeatedly breaks; uniform rules are the intended policy, and the link arrangement is the current imperfect mechanism.

The shared root Ruff file, its extension of `pyproject.toml`, and narrower Ruff configurations express the vertical and horizontal relationships described above. Uniformity of the baseline coexists with differences in the scope to which a rule applies.

References: [configuration provisioning](C:/apps/Z0Z_/makeSymlinks.cmd), [typing links](C:/apps/Z0Z_/linkTypings.cmd), [shared Ruff policy](C:/apps/hunterMakesPy/ruff.toml), and [archive specialization](C:/apps/mapFolding/archive/ruff.toml).

## Interpreting variation and external constraints

**Principle.** Read older code in light of the current system and the constraints under which it was written. A repository snapshot alone does not establish Hunter's present preference.

Hunter identifies three major sources of apparent exceptions: a newer system has not yet been applied to a project, external constraints affect the implementation, or learning more about programming. An assistant should establish that context before inferring a new rule from an exception.

Two corrections are particularly relevant to `astToolFactory`:

- `cpython/` and the versioned material in `data/` are ways of coping with upstream code and its quality, including a substantial lint burden in the imported code. Their organization must be understood in that context. Treating the arrangement solely as a clean, preferred architecture loses its motivation.
- The `src/` layout was a vestige of the uv build. Hunter dislikes that convention and moved the packages back. The recent moves out of `src/` express that correction; remaining instances do not by themselves establish a preference for `src/`.

Older assistant descriptions require the same care. The two coding-paradigm drafts in `Z0Z_/thoughts` contain broad claims that differ from the current skills, including prescriptions favoring functional programming, an overly broad treatment of semantic constants, and an absolute statement about configuration occupying one place. Use the current clarifications and current scoped guidance when reconciling that material.

## Permanent references and proposed destinations

The existing reference material already covers several principles. Additional explanations can be placed beside those rules and linked to the project examples, rather than copied into every repository's instructions.

| Topic                                                    | Existing reference or source                                                                                                                                                                              | Proposed disposition                                                                                                                                      |
| -------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Meaning before incidental representation                 | [Identifier standards](C:/Users/hunte/.codex/skills/python-identifiers/references/identifier-standards.md)                                                                                                | Preserve the ambiguity-driven motivation and the `Leaf` example beside the existing rules.                                                                |
| Responsibility and authority across scopes               | [Design coherence](C:/Users/hunte/.codex/skills/python-identifiers/references/design-coherence.md)                                                                                                        | Add the vertical/horizontal distinction and clarify how one principle can apply at several scales.                                                        |
| Structures that eliminate interpretation and bookkeeping | [Python code generation](C:/Users/hunte/.codex/skills/python-code-generation/SKILL.md) and [post-defensive computation](C:/Users/hunte/.codex/skills/python-code-generation/references/post-defensive.md) | Preserve the selector and disk examples in a linked design explanation, with their producer contracts and the work eliminated.                            |
| Runtime constructors and annotation-only imports         | [Type annotation guidance](C:/Users/hunte/.codex/skills/python-code-generation/references/type-annotations.md)                                                                                            | Link the selector records as a concrete example of runtime use.                                                                                           |
| Selector schema and its executor                         | [Dataframe update annex](C:/apps/astToolFactory/astToolFactory/datacenter/_dataframeUpdateAnnex.py) and [executor](C:/apps/astToolFactory/astToolFactory/datacenter/_dataframeUpdate.py:842)              | Retain implementation details locally; explain the batch-derived structural technique in a focused design reference.                                      |
| Project-specific coordinate meaning                      | [Semiotics guide](C:/apps/mapFolding/mapFolding/_semiotics.md) and [symbol guide](C:/apps/mapFolding/mapFolding/_symbols.md)                                                                              | Keep domain explanations with the package; link them as examples from general guidance.                                                                   |
| Shared policy and local link mechanics                   | [makeSymlinks.cmd](C:/apps/Z0Z_/makeSymlinks.cmd), [linkTypings.cmd](C:/apps/Z0Z_/linkTypings.cmd), and [authority files](C:/apps/hunterMakesPy/ruff.toml)                                                | Collect a shared configuration reference that identifies authority, inheritance, scope, link types, and the limits of the current synchronization script. |
| Older coding-paradigm summaries                          | The two coding-paradigm drafts under `C:\apps\Z0Z_\thoughts`                                                                                                                                              | Reconcile them with current clarifications before promoting any statements into current instructions.                                                     |
| Current astToolFactory organization                      | Its settings, datacenter, factory, filesystem, annex, snippet, and documentation modules                                                                                                                  | Describe actual responsibilities and external constraints in project documentation as the organization settles.                                           |

## Moving the material into durable guidance

The next documentation work can separate three things: principles useful across projects, mechanisms specific to a project, and historical examples that demonstrate a principle.

For each item moved, preserve its motivation, scope, example, and existing source. Update the appropriate longer-lived reference, then replace the corresponding explanation here with a short pointer. Keep an unresolved interpretation in these working notes until Hunter settles it. When implementation changes, update the mechanism's local documentation without losing the more general reason for the design.

The current document captures the survey and Hunter's corrections. It leaves the linked permanent references and project sources in place for that subsequent reconciliation.
