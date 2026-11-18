.PHONY: help status

help:
	@echo "Available targets:"
	@echo " make status  show git branch and working tree state"

status:
	@git branch --show-current
	@git status --short
	