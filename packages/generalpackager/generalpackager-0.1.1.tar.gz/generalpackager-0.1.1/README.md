# generalpackager
Tools to interface GitHub, PyPI and local modules / repos. Used for generating files to keep projects dry and synced. Tailored for my general packages.

This package and 3 other make up [ManderaGeneral](https://github.com/Mandera).

## Information
| Package                                                              | Version                                            | Latest Release       | Python                                                                                                                   | Platform        | Todos                                                        |   Hierarchy |
|:---------------------------------------------------------------------|:---------------------------------------------------|:---------------------|:-------------------------------------------------------------------------------------------------------------------------|:----------------|:-------------------------------------------------------------|------------:|
| [generalpackager](https://github.com/ManderaGeneral/generalpackager) | [0.1.1](https://pypi.org/project/generalpackager/) | 2021-02-05 12:37 CET | [3.8](https://www.python.org/downloads/release/python-380/), [3.9](https://www.python.org/downloads/release/python-390/) | Windows, Ubuntu | [16](https://github.com/ManderaGeneral/generalpackager#Todo) |           2 |

## Contents
<pre>
<a href='#generalpackager'>generalpackager</a>
├─ <a href='#Information'>Information</a>
├─ <a href='#Contents'>Contents</a>
├─ <a href='#Installation'>Installation</a>
├─ <a href='#Attributes'>Attributes</a>
└─ <a href='#Todo'>Todo</a>
</pre>

## Installation
| Command                       | <a href='https://pypi.org/project/pandas'>pandas</a>   | <a href='https://pypi.org/project/generallibrary'>generallibrary</a>   | <a href='https://pypi.org/project/generalfile'>generalfile</a>   | <a href='https://pypi.org/project/gitpython'>gitpython</a>   | <a href='https://pypi.org/project/requests'>requests</a>   |
|:------------------------------|:-------------------------------------------------------|:-----------------------------------------------------------------------|:-----------------------------------------------------------------|:-------------------------------------------------------------|:-----------------------------------------------------------|
| `pip install generalpackager` | Yes                                                    | Yes                                                                    | Yes                                                              | Yes                                                          | Yes                                                        |

## Attributes
<pre>
<a href='https://github.com/ManderaGeneral/generalpackager/blob/1e3b25d/generalpackager/__init__.py#L1'>Module: generalpackager</a>
├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/1e3b25d/generalpackager/api/github.py#L9'>Class: GitHub</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/1e3b25d/generalpackager/api/github.py#L37'>Method: api_url</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/1e3b25d/generalpackager/api/github.py#L65'>Method: get_description</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/1e3b25d/generalpackager/api/github.py#L52'>Method: get_topics</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/1e3b25d/generalpackager/api/github.py#L28'>Method: get_url</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/1e3b25d/generalpackager/api/github.py#L90'>Method: get_users_packages</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/1e3b25d/generalpackager/api/github.py#L41'>Method: get_website</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/1e3b25d/generalpackager/api/github.py#L23'>Method: is_creatable</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/1e3b25d/generalpackager/api/github.py#L33'>Method: is_url_functioning</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/1e3b25d/generalpackager/api/github.py#L71'>Method: set_description</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/1e3b25d/generalpackager/api/github.py#L58'>Method: set_topics</a>
│  └─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/1e3b25d/generalpackager/api/github.py#L47'>Method: set_website</a>
├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/1e3b25d/generalpackager/api/local_module.py#L8'>Class: LocalModule</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/1e3b25d/generalpackager/api/local_module.py#L43'>Method: get_all_packages</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/1e3b25d/generalpackager/api/local_module.py#L54'>Method: get_dependants</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/1e3b25d/generalpackager/api/local_module.py#L48'>Method: get_dependencies</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/1e3b25d/generalpackager/api/local_module.py#L34'>Method: get_env_vars</a>
│  └─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/1e3b25d/generalpackager/api/local_module.py#L20'>Method: is_creatable</a>
├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/1e3b25d/generalpackager/api/local_repo.py#L13'>Class: LocalRepo</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/1e3b25d/generalpackager/api/local_repo.py#L150'>Method: bump_version</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/1e3b25d/generalpackager/api/local_repo.py#L124'>Method: commit_and_push</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/1e3b25d/generalpackager/api/local_repo.py#L163'>Method: create_sdist</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/1e3b25d/generalpackager/api/local_repo.py#L145'>Method: get_changed_files</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/1e3b25d/generalpackager/api/local_repo.py#L80'>Method: get_git_exclude_path</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/1e3b25d/generalpackager/api/local_repo.py#L92'>Method: get_license_path</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/1e3b25d/generalpackager/api/local_repo.py#L108'>Method: get_local_repos</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/1e3b25d/generalpackager/api/local_repo.py#L88'>Method: get_manifest_path</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/1e3b25d/generalpackager/api/local_repo.py#L76'>Method: get_metadata_path</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/1e3b25d/generalpackager/api/local_repo.py#L104'>Method: get_package_paths</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/1e3b25d/generalpackager/api/local_repo.py#L72'>Method: get_readme_path</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/1e3b25d/generalpackager/api/local_repo.py#L45'>Method: get_repos_path</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/1e3b25d/generalpackager/api/local_repo.py#L84'>Method: get_setup_path</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/1e3b25d/generalpackager/api/local_repo.py#L100'>Method: get_test_path</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/1e3b25d/generalpackager/api/local_repo.py#L96'>Method: get_workflow_path</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/1e3b25d/generalpackager/api/local_repo.py#L58'>Method: is_creatable</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/1e3b25d/generalpackager/api/local_repo.py#L63'>Method: metadata_setter</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/1e3b25d/generalpackager/api/local_repo.py#L116'>Method: path_is_repo</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/1e3b25d/generalpackager/api/local_repo.py#L154'>Method: pip_install</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/1e3b25d/generalpackager/api/local_repo.py#L159'>Method: unittest</a>
│  └─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/1e3b25d/generalpackager/api/local_repo.py#L168'>Method: upload</a>
├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/1e3b25d/generalpackager/packager.py#L17'>Class: Packager</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/1e3b25d/generalpackager/api/github.py#L9'>Class: GitHub</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/1e3b25d/generalpackager/api/local_module.py#L8'>Class: LocalModule</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/1e3b25d/generalpackager/api/local_repo.py#L13'>Class: LocalRepo</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/1e3b25d/generalpackager/api/pypi.py#L27'>Class: PyPI</a>
│  │  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/1e3b25d/generalpackager/api/pypi.py#L53'>Method: download_and_unpack_tarball</a>
│  │  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/1e3b25d/generalpackager/api/pypi.py#L77'>Method: get_datetime</a>
│  │  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/1e3b25d/generalpackager/api/pypi.py#L44'>Method: get_tarball_url</a>
│  │  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/1e3b25d/generalpackager/api/pypi.py#L39'>Method: get_url</a>
│  │  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/1e3b25d/generalpackager/api/pypi.py#L61'>Method: get_users_packages</a>
│  │  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/1e3b25d/generalpackager/api/pypi.py#L69'>Method: get_version</a>
│  │  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/1e3b25d/generalpackager/api/pypi.py#L34'>Method: is_creatable</a>
│  │  └─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/1e3b25d/generalpackager/api/pypi.py#L86'>Method: reserve_name</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/1e3b25d/generalpackager/packager_relations.py#L6'>Method: add</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/1e3b25d/generalpackager/packager_github.py#L19'>Method: clone_repo</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/1e3b25d/generalpackager/packager_github.py#L31'>Method: commit_push_store_sha</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/1e3b25d/generalpackager/packager_pypi.py#L6'>Method: compare_local_to_pypi</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/1e3b25d/generalpackager/packager_files.py#L79'>Method: compare_local_to_remote</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/1e3b25d/generalpackager/packager_markdown.py#L108'>Method: configure_contents_markdown</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/1e3b25d/generalpackager/packager_files.py#L59'>Method: filter_relative_filenames</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/1e3b25d/generalpackager/packager_relations.py#L85'>Method: general_bumped_set</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/1e3b25d/generalpackager/packager_relations.py#L92'>Method: general_changed_dict</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/1e3b25d/generalpackager/packager_files.py#L143'>Method: generate_git_exclude</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/1e3b25d/generalpackager/packager_files.py#L149'>Method: generate_license</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/1e3b25d/generalpackager/packager.py#L91'>Method: generate_localfiles</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/1e3b25d/generalpackager/packager_files.py#L134'>Method: generate_manifest</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/1e3b25d/generalpackager/packager_files.py#L209'>Method: generate_personal_readme</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/1e3b25d/generalpackager/packager_files.py#L177'>Method: generate_readme</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/1e3b25d/generalpackager/packager_files.py#L86'>Method: generate_setup</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/1e3b25d/generalpackager/packager_files.py#L161'>Method: generate_workflow</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/1e3b25d/generalpackager/packager_markdown.py#L145'>Method: get_attributes_markdown</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/1e3b25d/generalpackager/packager_markdown.py#L11'>Method: get_badges_dict</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/1e3b25d/generalpackager/packager_metadata.py#L26'>Method: get_classifiers</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/1e3b25d/generalpackager/packager_relations.py#L58'>Method: get_dependencies</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/1e3b25d/generalpackager/packager_relations.py#L64'>Method: get_dependents</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/1e3b25d/generalpackager/packager_markdown.py#L50'>Method: get_description_markdown</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/1e3b25d/generalpackager/packager_workflow.py#L71'>Method: get_env</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/1e3b25d/generalpackager/packager_markdown.py#L152'>Method: get_footnote_markdown</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/1e3b25d/generalpackager/packager_markdown.py#L58'>Method: get_information_markdown</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/1e3b25d/generalpackager/packager_markdown.py#L83'>Method: get_installation_markdown</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/1e3b25d/generalpackager/packager_relations.py#L70'>Method: get_ordered_packagers</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/1e3b25d/generalpackager/packager_relations.py#L31'>Method: get_packager_with_name</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/1e3b25d/generalpackager/packager_workflow.py#L30'>Method: get_step</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/1e3b25d/generalpackager/packager_workflow.py#L106'>Method: get_sync_job</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/1e3b25d/generalpackager/packager_markdown.py#L23'>Method: get_todos</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/1e3b25d/generalpackager/packager_metadata.py#L16'>Method: get_topics</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/1e3b25d/generalpackager/packager_workflow.py#L22'>Method: get_triggers</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/1e3b25d/generalpackager/packager_workflow.py#L92'>Method: get_unittest_job</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/1e3b25d/generalpackager/packager_relations.py#L76'>Method: get_users_package_names</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/1e3b25d/generalpackager/packager_markdown.py#L117'>Method: github_link</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/1e3b25d/generalpackager/packager_markdown.py#L124'>Method: github_link_path_line</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/1e3b25d/generalpackager/packager_workflow.py#L160'>Method: if_publish_bump</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/1e3b25d/generalpackager/packager_workflow.py#L165'>Method: if_publish_publish</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/1e3b25d/generalpackager/packager_metadata.py#L32'>Method: is_bumped</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/1e3b25d/generalpackager/packager.py#L50'>Method: is_creatable</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/1e3b25d/generalpackager/packager_relations.py#L45'>Method: load_general_packagers</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/1e3b25d/generalpackager/packager_files.py#L46'>Method: relative_path_is_aesthetic</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/1e3b25d/generalpackager/packager_relations.py#L15'>Method: remove</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/1e3b25d/generalpackager/packager_workflow.py#L122'>Method: run_ordered_methods</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/1e3b25d/generalpackager/packager_workflow.py#L45'>Method: step_install_necessities</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/1e3b25d/generalpackager/packager_workflow.py#L59'>Method: step_install_package_git</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/1e3b25d/generalpackager/packager_workflow.py#L52'>Method: step_install_package_pip</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/1e3b25d/generalpackager/packager_workflow.py#L115'>Method: step_run_packager_method</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/1e3b25d/generalpackager/packager_workflow.py#L38'>Method: step_setup_python</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/1e3b25d/generalpackager/packager_workflow.py#L82'>Method: steps_setup</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/1e3b25d/generalpackager/packager_github.py#L11'>Method: sync_github_metadata</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/1e3b25d/generalpackager/packager_relations.py#L21'>Method: update_links</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/1e3b25d/generalpackager/packager_workflow.py#L138'>Method: workflow_sync</a>
│  └─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/1e3b25d/generalpackager/packager_workflow.py#L130'>Method: workflow_unittest</a>
└─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/1e3b25d/generalpackager/api/pypi.py#L27'>Class: PyPI</a>
</pre>

## Todo
| Module                                                                                                                                   | Message                                                                                                                                                                                                  |
|:-----------------------------------------------------------------------------------------------------------------------------------------|:---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| <a href='https://github.com/ManderaGeneral/generalpackager/blob/master/randomtesting.py#L1'>randomtesting.py</a>                         | <a href='https://github.com/ManderaGeneral/generalpackager/blob/master/randomtesting.py#L72'>Install packages in correct order when using git to prevent it using pip.</a>                               |
| <a href='https://github.com/ManderaGeneral/generalpackager/blob/master/randomtesting.py#L1'>randomtesting.py</a>                         | <a href='https://github.com/ManderaGeneral/generalpackager/blob/master/randomtesting.py#L74'>Write [CI MAJOR] in commit message to bump major for example.</a>                                           |
| <a href='https://github.com/ManderaGeneral/generalpackager/blob/master/randomtesting.py#L1'>randomtesting.py</a>                         | <a href='https://github.com/ManderaGeneral/generalpackager/blob/master/randomtesting.py#L75'>Push empty commits to dependents after publish in workflow.</a>                                             |
| <a href='https://github.com/ManderaGeneral/generalpackager/blob/master/randomtesting.py#L1'>randomtesting.py</a>                         | <a href='https://github.com/ManderaGeneral/generalpackager/blob/master/randomtesting.py#L76'>Generate GitHub profile readme.</a>                                                                         |
| <a href='https://github.com/ManderaGeneral/generalpackager/blob/master/randomtesting.py#L1'>randomtesting.py</a>                         | <a href='https://github.com/ManderaGeneral/generalpackager/blob/master/randomtesting.py#L77'>Compare local\_repo version with pypi version before publishing.</a>                                         |
| <a href='https://github.com/ManderaGeneral/generalpackager/blob/master/generalpackager/packager\_markdown.py#L1'>packager\_markdown.py</a> | <a href='https://github.com/ManderaGeneral/generalpackager/blob/master/generalpackager/packager\_markdown.py#L10'>Inherit future crawler class for pypi and github.</a>                                   |
| <a href='https://github.com/ManderaGeneral/generalpackager/blob/master/generalpackager/packager\_grp.py#L1'>packager\_grp.py</a>           | <a href='https://github.com/ManderaGeneral/generalpackager/blob/master/generalpackager/packager\_grp.py#L15'>Maybe move PackagerGrp to Packager now that it inherits NetworkDiagram?</a>                  |
| <a href='https://github.com/ManderaGeneral/generalpackager/blob/master/generalpackager/packager.py#L1'>packager.py</a>                   | <a href='https://github.com/ManderaGeneral/generalpackager/blob/master/generalpackager/packager.py#L20'>Allow github, pypi or local repo not to exist in any combination.</a>                            |
| <a href='https://github.com/ManderaGeneral/generalpackager/blob/master/generalpackager/packager.py#L1'>packager.py</a>                   | <a href='https://github.com/ManderaGeneral/generalpackager/blob/master/generalpackager/packager.py#L21'>Replace badges with generated hardcode.</a>                                                      |
| <a href='https://github.com/ManderaGeneral/generalpackager/blob/master/generalpackager/packager.py#L1'>packager.py</a>                   | <a href='https://github.com/ManderaGeneral/generalpackager/blob/master/generalpackager/packager.py#L22'>Find all imports to generate install\_requires.</a>                                               |
| <a href='https://github.com/ManderaGeneral/generalpackager/blob/master/generalpackager/packager.py#L1'>packager.py</a>                   | <a href='https://github.com/ManderaGeneral/generalpackager/blob/master/generalpackager/packager.py#L23'>Create links for Todos.</a>                                                                      |
| <a href='https://github.com/ManderaGeneral/generalpackager/blob/master/generalpackager/packager\_files.py#L1'>packager\_files.py</a>       | <a href='https://github.com/ManderaGeneral/generalpackager/blob/master/generalpackager/packager\_files.py#L30'>Watermark generated files to prevent mistake of thinking you can modify them directly.</a> |
| <a href='https://github.com/ManderaGeneral/generalpackager/blob/master/generalpackager/api/pypi.py#L1'>pypi.py</a>                       | <a href='https://github.com/ManderaGeneral/generalpackager/blob/master/generalpackager/api/pypi.py#L11'>Move download to it's own package.</a>                                                           |
| <a href='https://github.com/ManderaGeneral/generalpackager/blob/master/generalpackager/api/pypi.py#L1'>pypi.py</a>                       | <a href='https://github.com/ManderaGeneral/generalpackager/blob/master/generalpackager/api/pypi.py#L12'>Binary extension for generalfile.</a>                                                            |
| <a href='https://github.com/ManderaGeneral/generalpackager/blob/master/generalpackager/api/pypi.py#L1'>pypi.py</a>                       | <a href='https://github.com/ManderaGeneral/generalpackager/blob/master/generalpackager/api/pypi.py#L23'>Add pack and unpack to generalfile.</a>                                                          |
| <a href='https://github.com/ManderaGeneral/generalpackager/blob/master/generalpackager/api/pypi.py#L1'>pypi.py</a>                       | <a href='https://github.com/ManderaGeneral/generalpackager/blob/master/generalpackager/api/pypi.py#L79'>Proper date fetch.</a>                                                                           |

<sup>
Generated 2021-02-05 18:47 CET for commit <a href='https://github.com/ManderaGeneral/generalpackager/commit/1e3b25d'>1e3b25d</a>.
</sup>
