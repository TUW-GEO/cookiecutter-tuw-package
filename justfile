_default:
	@just --list

alias t:= test


# run the test suite
test:
	uv run pytest tests/
