# COLORS
GREEN  := $(shell tput -Txterm setaf 2)
WHITE  := $(shell tput -Txterm setaf 7)
YELLOW := $(shell tput -Txterm setaf 3)
RESET  := $(shell tput -Txterm sgr0)

.DEFAULT_GOAL := help
.PHONY: help format lint check-style check-import-sorting lint-typing lint-imports lint-complexity lint-deps

PY_TARGET_DIRS=src

## Отформатировать код
format:
	autoflake --recursive $(PY_TARGET_DIRS) --in-place --remove-unused-variables --remove-all-unused-imports --ignore-init-module-imports --remove-duplicate-keys --ignore-pass-statements
	pyup_dirs --py311-plus $(PY_TARGET_DIRS) | true
	isort --color --quiet $(PY_TARGET_DIRS)
	black $(PY_TARGET_DIRS)

## Проверить стилистику кода
check-style:
	black --check $(PY_TARGET_DIRS)

## Проверить сортировку импортов
check-import-sorting:
	isort --check-only $(PY_TARGET_DIRS)

## Проверить типизацию
lint-typing:
	mypy $(PY_TARGET_DIRS)

## Проверить код на сложность
lint-complexity:
	flake8 $(PY_TARGET_DIRS)

## Запустить линтер ruff
lint-ruff:
	ruff $(PY_TARGET_DIRS)

## Проверить зависимостей
lint-deps:
	poetry run poetry check
	poetry run pip check
	poetry run safety check --full-report
	poetry run pip-audit

## Запустить все линтеры
lint: lint-ruff lint-typing lint-complexity check-import-sorting lint-deps

## Show help
help:
	@echo ''
	@echo 'Usage:'
	@echo '  ${YELLOW}make${RESET} ${GREEN}<target>${RESET}'
	@echo ''
	@echo 'Targets:'
	@awk '/^[a-zA-Z\-_0-9]+:/ { \
		helpMessage = match(lastLine, /^## (.*)/); \
		if (helpMessage) { \
			helpCommand = $$1; sub(/:$$/, "", helpCommand); \
			helpMessage = substr(lastLine, RSTART + 3, RLENGTH); \
			printf "  ${YELLOW}%-$(TARGET_MAX_CHAR_NUM)25s${RESET} ${GREEN}%s${RESET}\n", helpCommand, helpMessage; \
		} \
	} \
	{ lastLine = $$0 }' $(MAKEFILE_LIST)
	@echo ''
