# generalpackager
Tools to interface GitHub, PyPI and local modules / repos. Used for generating files to keep projects dry and synced. Tailored for my general packages.

This package and 3 other make up [ManderaGeneral](https://github.com/Mandera).

## Information
| Package                                                              | Version                                            | Latest Release       | Python                                                                                                                   | Platform        | Todos                                                        |   Hierarchy |
|:---------------------------------------------------------------------|:---------------------------------------------------|:---------------------|:-------------------------------------------------------------------------------------------------------------------------|:----------------|:-------------------------------------------------------------|------------:|
| [generalpackager](https://github.com/ManderaGeneral/generalpackager) | [0.1.2](https://pypi.org/project/generalpackager/) | 2021-02-05 18:47 CET | [3.8](https://www.python.org/downloads/release/python-380/), [3.9](https://www.python.org/downloads/release/python-390/) | Windows, Ubuntu | [16](https://github.com/ManderaGeneral/generalpackager#Todo) |           2 |

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
<a href='https://github.com/ManderaGeneral/generalpackager/blob/49aec45/generalpackager/__init__.py#L1'>Module: generalpackager</a>
└─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/49aec45/generalpackager/packager.py#L20'>Class: Packager</a>
   ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/49aec45/generalpackager/api/github.py#L9'>Class: GitHub</a>
   │  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/49aec45/generalpackager/api/github.py#L37'>Method: api_url</a> <b>(Untested)</b>
   │  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/49aec45/generalpackager/api/github.py#L65'>Method: get_description</a> <b>(Untested)</b>
   │  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/49aec45/generalpackager/api/github.py#L52'>Method: get_topics</a>
   │  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/49aec45/generalpackager/api/github.py#L28'>Method: get_url</a> <b>(Untested)</b>
   │  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/49aec45/generalpackager/api/github.py#L90'>Method: get_users_packages</a> <b>(Untested)</b>
   │  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/49aec45/generalpackager/api/github.py#L41'>Method: get_website</a> <b>(Untested)</b>
   │  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/49aec45/generalpackager/api/github.py#L23'>Method: is_creatable</a> <b>(Untested)</b>
   │  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/49aec45/generalpackager/api/github.py#L33'>Method: is_url_functioning</a> <b>(Untested)</b>
   │  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/49aec45/generalpackager/api/github.py#L71'>Method: set_description</a> <b>(Untested)</b>
   │  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/49aec45/generalpackager/api/github.py#L58'>Method: set_topics</a> <b>(Untested)</b>
   │  └─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/49aec45/generalpackager/api/github.py#L47'>Method: set_website</a> <b>(Untested)</b>
   ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/49aec45/generalpackager/api/local_module.py#L8'>Class: LocalModule</a> <b>(Untested)</b>
   │  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/49aec45/generalpackager/api/local_module.py#L43'>Method: get_all_packages</a> <b>(Untested)</b>
   │  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/49aec45/generalpackager/api/local_module.py#L54'>Method: get_dependants</a> <b>(Untested)</b>
   │  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/49aec45/generalpackager/api/local_module.py#L48'>Method: get_dependencies</a> <b>(Untested)</b>
   │  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/49aec45/generalpackager/api/local_module.py#L34'>Method: get_env_vars</a> <b>(Untested)</b>
   │  └─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/49aec45/generalpackager/api/local_module.py#L20'>Method: is_creatable</a> <b>(Untested)</b>
   ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/49aec45/generalpackager/api/local_repo.py#L13'>Class: LocalRepo</a> <b>(Untested)</b>
   │  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/49aec45/generalpackager/api/local_repo.py#L162'>Method: bump_version</a> <b>(Untested)</b>
   │  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/49aec45/generalpackager/api/local_repo.py#L136'>Method: commit_and_push</a> <b>(Untested)</b>
   │  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/49aec45/generalpackager/api/local_repo.py#L175'>Method: create_sdist</a> <b>(Untested)</b>
   │  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/49aec45/generalpackager/api/local_repo.py#L157'>Method: get_changed_files</a> <b>(Untested)</b>
   │  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/49aec45/generalpackager/api/local_repo.py#L80'>Method: get_git_exclude_path</a> <b>(Untested)</b>
   │  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/49aec45/generalpackager/api/local_repo.py#L92'>Method: get_license_path</a> <b>(Untested)</b>
   │  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/49aec45/generalpackager/api/local_repo.py#L120'>Method: get_local_repos</a> <b>(Untested)</b>
   │  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/49aec45/generalpackager/api/local_repo.py#L88'>Method: get_manifest_path</a> <b>(Untested)</b>
   │  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/49aec45/generalpackager/api/local_repo.py#L76'>Method: get_metadata_path</a> <b>(Untested)</b>
   │  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/49aec45/generalpackager/api/local_repo.py#L116'>Method: get_package_paths</a> <b>(Untested)</b>
   │  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/49aec45/generalpackager/api/local_repo.py#L72'>Method: get_readme_path</a> <b>(Untested)</b>
   │  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/49aec45/generalpackager/api/local_repo.py#L45'>Method: get_repos_path</a> <b>(Untested)</b>
   │  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/49aec45/generalpackager/api/local_repo.py#L84'>Method: get_setup_path</a> <b>(Untested)</b>
   │  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/49aec45/generalpackager/api/local_repo.py#L100'>Method: get_test_path</a> <b>(Untested)</b>
   │  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/49aec45/generalpackager/api/local_repo.py#L104'>Method: get_test_paths</a> <b>(Untested)</b>
   │  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/49aec45/generalpackager/api/local_repo.py#L96'>Method: get_workflow_path</a> <b>(Untested)</b>
   │  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/49aec45/generalpackager/api/local_repo.py#L58'>Method: is_creatable</a> <b>(Untested)</b>
   │  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/49aec45/generalpackager/api/local_repo.py#L63'>Method: metadata_setter</a> <b>(Untested)</b>
   │  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/49aec45/generalpackager/api/local_repo.py#L128'>Method: path_is_repo</a> <b>(Untested)</b>
   │  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/49aec45/generalpackager/api/local_repo.py#L166'>Method: pip_install</a> <b>(Untested)</b>
   │  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/49aec45/generalpackager/api/local_repo.py#L109'>Method: text_in_tests</a> <b>(Untested)</b>
   │  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/49aec45/generalpackager/api/local_repo.py#L171'>Method: unittest</a>
   │  └─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/49aec45/generalpackager/api/local_repo.py#L180'>Method: upload</a> <b>(Untested)</b>
   ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/49aec45/generalpackager/api/pypi.py#L27'>Class: PyPI</a> <b>(Untested)</b>
   │  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/49aec45/generalpackager/api/pypi.py#L53'>Method: download_and_unpack_tarball</a> <b>(Untested)</b>
   │  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/49aec45/generalpackager/api/pypi.py#L77'>Method: get_datetime</a> <b>(Untested)</b>
   │  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/49aec45/generalpackager/api/pypi.py#L44'>Method: get_tarball_url</a> <b>(Untested)</b>
   │  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/49aec45/generalpackager/api/pypi.py#L39'>Method: get_url</a> <b>(Untested)</b>
   │  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/49aec45/generalpackager/api/pypi.py#L61'>Method: get_users_packages</a> <b>(Untested)</b>
   │  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/49aec45/generalpackager/api/pypi.py#L69'>Method: get_version</a> <b>(Untested)</b>
   │  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/49aec45/generalpackager/api/pypi.py#L34'>Method: is_creatable</a> <b>(Untested)</b>
   │  └─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/49aec45/generalpackager/api/pypi.py#L86'>Method: reserve_name</a> <b>(Untested)</b>
   ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/49aec45/generalpackager/packager_relations.py#L6'>Method: add</a> <b>(Untested)</b>
   ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/49aec45/generalpackager/packager_github.py#L19'>Method: clone_repo</a> <b>(Untested)</b>
   ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/49aec45/generalpackager/packager_github.py#L31'>Method: commit_push_store_sha</a> <b>(Untested)</b>
   ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/49aec45/generalpackager/packager_pypi.py#L6'>Method: compare_local_to_pypi</a> <b>(Untested)</b>
   ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/49aec45/generalpackager/packager_files.py#L79'>Method: compare_local_to_remote</a> <b>(Untested)</b>
   ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/49aec45/generalpackager/packager_markdown.py#L108'>Method: configure_contents_markdown</a> <b>(Untested)</b>
   ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/49aec45/generalpackager/packager_files.py#L59'>Method: filter_relative_filenames</a> <b>(Untested)</b>
   ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/49aec45/generalpackager/packager_relations.py#L85'>Method: general_bumped_set</a> <b>(Untested)</b>
   ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/49aec45/generalpackager/packager_relations.py#L92'>Method: general_changed_dict</a> <b>(Untested)</b>
   ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/49aec45/generalpackager/packager_files.py#L143'>Method: generate_git_exclude</a> <b>(Untested)</b>
   ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/49aec45/generalpackager/packager_files.py#L149'>Method: generate_license</a> <b>(Untested)</b>
   ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/49aec45/generalpackager/packager.py#L94'>Method: generate_localfiles</a> <b>(Untested)</b>
   ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/49aec45/generalpackager/packager_files.py#L134'>Method: generate_manifest</a> <b>(Untested)</b>
   ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/49aec45/generalpackager/packager_files.py#L209'>Method: generate_personal_readme</a> <b>(Untested)</b>
   ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/49aec45/generalpackager/packager_files.py#L177'>Method: generate_readme</a> <b>(Untested)</b>
   ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/49aec45/generalpackager/packager_files.py#L86'>Method: generate_setup</a> <b>(Untested)</b>
   ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/49aec45/generalpackager/packager_files.py#L161'>Method: generate_workflow</a> <b>(Untested)</b>
   ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/49aec45/generalpackager/packager_markdown.py#L149'>Method: get_attributes_markdown</a> <b>(Untested)</b>
   ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/49aec45/generalpackager/packager_markdown.py#L11'>Method: get_badges_dict</a> <b>(Untested)</b>
   ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/49aec45/generalpackager/packager_metadata.py#L26'>Method: get_classifiers</a> <b>(Untested)</b>
   ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/49aec45/generalpackager/packager_relations.py#L58'>Method: get_dependencies</a> <b>(Untested)</b>
   ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/49aec45/generalpackager/packager_relations.py#L64'>Method: get_dependents</a> <b>(Untested)</b>
   ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/49aec45/generalpackager/packager_markdown.py#L50'>Method: get_description_markdown</a> <b>(Untested)</b>
   ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/49aec45/generalpackager/packager_workflow.py#L71'>Method: get_env</a> <b>(Untested)</b>
   ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/49aec45/generalpackager/packager_markdown.py#L156'>Method: get_footnote_markdown</a> <b>(Untested)</b>
   ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/49aec45/generalpackager/packager_markdown.py#L58'>Method: get_information_markdown</a> <b>(Untested)</b>
   ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/49aec45/generalpackager/packager_markdown.py#L83'>Method: get_installation_markdown</a> <b>(Untested)</b>
   ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/49aec45/generalpackager/packager_relations.py#L70'>Method: get_ordered_packagers</a> <b>(Untested)</b>
   ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/49aec45/generalpackager/packager_relations.py#L31'>Method: get_packager_with_name</a> <b>(Untested)</b>
   ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/49aec45/generalpackager/packager_workflow.py#L30'>Method: get_step</a> <b>(Untested)</b>
   ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/49aec45/generalpackager/packager_workflow.py#L106'>Method: get_sync_job</a> <b>(Untested)</b>
   ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/49aec45/generalpackager/packager_markdown.py#L23'>Method: get_todos</a> <b>(Untested)</b>
   ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/49aec45/generalpackager/packager_metadata.py#L16'>Method: get_topics</a>
   ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/49aec45/generalpackager/packager_workflow.py#L22'>Method: get_triggers</a> <b>(Untested)</b>
   ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/49aec45/generalpackager/packager_workflow.py#L92'>Method: get_unittest_job</a> <b>(Untested)</b>
   ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/49aec45/generalpackager/packager_relations.py#L76'>Method: get_users_package_names</a> <b>(Untested)</b>
   ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/49aec45/generalpackager/packager_markdown.py#L117'>Method: github_link</a> <b>(Untested)</b>
   ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/49aec45/generalpackager/packager_markdown.py#L124'>Method: github_link_path_line</a> <b>(Untested)</b>
   ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/49aec45/generalpackager/packager_workflow.py#L160'>Method: if_publish_bump</a> <b>(Untested)</b>
   ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/49aec45/generalpackager/packager_workflow.py#L165'>Method: if_publish_publish</a> <b>(Untested)</b>
   ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/49aec45/generalpackager/packager_metadata.py#L32'>Method: is_bumped</a> <b>(Untested)</b>
   ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/49aec45/generalpackager/packager.py#L53'>Method: is_creatable</a> <b>(Untested)</b>
   ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/49aec45/generalpackager/packager_relations.py#L45'>Method: load_general_packagers</a> <b>(Untested)</b>
   ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/49aec45/generalpackager/packager_files.py#L46'>Method: relative_path_is_aesthetic</a> <b>(Untested)</b>
   ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/49aec45/generalpackager/packager_relations.py#L15'>Method: remove</a> <b>(Untested)</b>
   ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/49aec45/generalpackager/packager_workflow.py#L122'>Method: run_ordered_methods</a> <b>(Untested)</b>
   ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/49aec45/generalpackager/packager_workflow.py#L45'>Method: step_install_necessities</a> <b>(Untested)</b>
   ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/49aec45/generalpackager/packager_workflow.py#L59'>Method: step_install_package_git</a> <b>(Untested)</b>
   ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/49aec45/generalpackager/packager_workflow.py#L52'>Method: step_install_package_pip</a> <b>(Untested)</b>
   ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/49aec45/generalpackager/packager_workflow.py#L115'>Method: step_run_packager_method</a> <b>(Untested)</b>
   ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/49aec45/generalpackager/packager_workflow.py#L38'>Method: step_setup_python</a> <b>(Untested)</b>
   ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/49aec45/generalpackager/packager_workflow.py#L82'>Method: steps_setup</a> <b>(Untested)</b>
   ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/49aec45/generalpackager/packager_github.py#L11'>Method: sync_github_metadata</a> <b>(Untested)</b>
   ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/49aec45/generalpackager/packager_relations.py#L21'>Method: update_links</a> <b>(Untested)</b>
   ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/49aec45/generalpackager/packager_workflow.py#L138'>Method: workflow_sync</a> <b>(Untested)</b>
   └─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/49aec45/generalpackager/packager_workflow.py#L130'>Method: workflow_unittest</a> <b>(Untested)</b>
</pre>

## Todo
| Module                                                                                                                                   | Message                                                                                                                                                                                                  |
|:-----------------------------------------------------------------------------------------------------------------------------------------|:---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| <a href='https://github.com/ManderaGeneral/generalpackager/blob/master/randomtesting.py#L1'>randomtesting.py</a>                         | <a href='https://github.com/ManderaGeneral/generalpackager/blob/master/randomtesting.py#L86'>Install packages in correct order when using git to prevent it using pip.</a>                               |
| <a href='https://github.com/ManderaGeneral/generalpackager/blob/master/randomtesting.py#L1'>randomtesting.py</a>                         | <a href='https://github.com/ManderaGeneral/generalpackager/blob/master/randomtesting.py#L88'>Write [CI MAJOR] in commit message to bump major for example.</a>                                           |
| <a href='https://github.com/ManderaGeneral/generalpackager/blob/master/randomtesting.py#L1'>randomtesting.py</a>                         | <a href='https://github.com/ManderaGeneral/generalpackager/blob/master/randomtesting.py#L89'>Push empty commits to dependents after publish in workflow.</a>                                             |
| <a href='https://github.com/ManderaGeneral/generalpackager/blob/master/randomtesting.py#L1'>randomtesting.py</a>                         | <a href='https://github.com/ManderaGeneral/generalpackager/blob/master/randomtesting.py#L90'>Generate GitHub profile readme.</a>                                                                         |
| <a href='https://github.com/ManderaGeneral/generalpackager/blob/master/randomtesting.py#L1'>randomtesting.py</a>                         | <a href='https://github.com/ManderaGeneral/generalpackager/blob/master/randomtesting.py#L91'>Compare local\_repo version with pypi version before publishing.</a>                                         |
| <a href='https://github.com/ManderaGeneral/generalpackager/blob/master/generalpackager/packager\_markdown.py#L1'>packager\_markdown.py</a> | <a href='https://github.com/ManderaGeneral/generalpackager/blob/master/generalpackager/packager\_markdown.py#L10'>Inherit future crawler class for pypi and github.</a>                                   |
| <a href='https://github.com/ManderaGeneral/generalpackager/blob/master/generalpackager/packager\_grp.py#L1'>packager\_grp.py</a>           | <a href='https://github.com/ManderaGeneral/generalpackager/blob/master/generalpackager/packager\_grp.py#L15'>Maybe move PackagerGrp to Packager now that it inherits NetworkDiagram?</a>                  |
| <a href='https://github.com/ManderaGeneral/generalpackager/blob/master/generalpackager/packager.py#L1'>packager.py</a>                   | <a href='https://github.com/ManderaGeneral/generalpackager/blob/master/generalpackager/packager.py#L23'>Allow github, pypi or local repo not to exist in any combination.</a>                            |
| <a href='https://github.com/ManderaGeneral/generalpackager/blob/master/generalpackager/packager.py#L1'>packager.py</a>                   | <a href='https://github.com/ManderaGeneral/generalpackager/blob/master/generalpackager/packager.py#L24'>Replace badges with generated hardcode.</a>                                                      |
| <a href='https://github.com/ManderaGeneral/generalpackager/blob/master/generalpackager/packager.py#L1'>packager.py</a>                   | <a href='https://github.com/ManderaGeneral/generalpackager/blob/master/generalpackager/packager.py#L25'>Find all imports to generate install\_requires.</a>                                               |
| <a href='https://github.com/ManderaGeneral/generalpackager/blob/master/generalpackager/packager.py#L1'>packager.py</a>                   | <a href='https://github.com/ManderaGeneral/generalpackager/blob/master/generalpackager/packager.py#L26'>Create links for Todos.</a>                                                                      |
| <a href='https://github.com/ManderaGeneral/generalpackager/blob/master/generalpackager/packager\_files.py#L1'>packager\_files.py</a>       | <a href='https://github.com/ManderaGeneral/generalpackager/blob/master/generalpackager/packager\_files.py#L30'>Watermark generated files to prevent mistake of thinking you can modify them directly.</a> |
| <a href='https://github.com/ManderaGeneral/generalpackager/blob/master/generalpackager/api/pypi.py#L1'>pypi.py</a>                       | <a href='https://github.com/ManderaGeneral/generalpackager/blob/master/generalpackager/api/pypi.py#L11'>Move download to it's own package.</a>                                                           |
| <a href='https://github.com/ManderaGeneral/generalpackager/blob/master/generalpackager/api/pypi.py#L1'>pypi.py</a>                       | <a href='https://github.com/ManderaGeneral/generalpackager/blob/master/generalpackager/api/pypi.py#L12'>Binary extension for generalfile.</a>                                                            |
| <a href='https://github.com/ManderaGeneral/generalpackager/blob/master/generalpackager/api/pypi.py#L1'>pypi.py</a>                       | <a href='https://github.com/ManderaGeneral/generalpackager/blob/master/generalpackager/api/pypi.py#L23'>Add pack and unpack to generalfile.</a>                                                          |
| <a href='https://github.com/ManderaGeneral/generalpackager/blob/master/generalpackager/api/pypi.py#L1'>pypi.py</a>                       | <a href='https://github.com/ManderaGeneral/generalpackager/blob/master/generalpackager/api/pypi.py#L79'>Proper date fetch.</a>                                                                           |

<sup>
Generated 2021-02-07 09:01 CET for commit <a href='https://github.com/ManderaGeneral/generalpackager/commit/49aec45'>49aec45</a>.
</sup>
