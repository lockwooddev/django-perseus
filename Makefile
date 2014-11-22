tests:
	py.test $(APP)

test:
	py.test -k $(test)

test_class:
	py.test $(path)

coverage:
	py.test --cov=$(APP) --cov-report=term-missing $(APP)

coverage-html:
	coverage run `which py.test` ${APP}
	coverage html -d htmlcov --include=django_perseus* --omit='*/tests*,*__init__*'
