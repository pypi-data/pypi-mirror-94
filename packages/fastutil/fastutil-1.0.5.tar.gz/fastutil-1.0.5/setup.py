from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

with open("requirements.txt", "r") as fr:
    requirements_list = [line.strip() for line in fr.readlines()]

setup(
    name='fastutil',
    version='1.0.5',
    description='常用python工具',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='kylin',
    author_email='464840061@qq.com',
    url='https://github.com/kylinat2688/fastutil',
    python_requires=">=3.4.0",
    install_requires=requirements_list,
    packages=find_packages(),
    entry_points={
        "console_scripts": [
            "taskplan = fastutil.task_plan:start_plan",
            "taskkill = fastutil.task_util:kill_task",
            "fitlog_init= fastutil.model_util:init_fitlog",
            "fitlog_commit= fastutil.model_util:fitlog_commit",
            "ver_id= fastutil.model_util:ver_id",
            "date_ver_id= fastutil.model_util:date_ver_id"
        ]
    }
)
