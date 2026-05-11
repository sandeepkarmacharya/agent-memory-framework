# Coding Standards

## General rules

- Prefer simple code over clever code.
- Keep changes small and focused.
- Avoid unrelated refactors during feature work.
- Name files, functions, and concepts using the shared language in `.ai/shared-language.md`.
- Do not create abstractions before they are needed.

## File and module rules

- Keep files readable and cohesive.
- Split files when they mix unrelated responsibilities.
- Prefer deep modules with small external interfaces.
- Avoid circular dependencies.

## Testing rules

- Add tests for important business logic.
- For bugs, create or describe a regression check.
- If tests cannot be run, explain why and mark validation as unverified.

## Error handling

- Handle expected errors explicitly.
- Do not swallow exceptions silently.
- Show useful messages without leaking sensitive data.

## Security rules

- Never commit API keys, tokens, passwords, or private credentials.
- Validate inputs at trust boundaries.
- Avoid logging sensitive data.
- Keep auth and permission checks close to protected operations.

## Accessibility rules

- Use semantic HTML where applicable.
- Ensure keyboard access for interactive UI.
- Use clear labels and states.

## Agent behavior rules

- Read memory before coding.
- Do not restart from scratch.
- Update memory after meaningful work.
- Prefer minimal safe changes.
