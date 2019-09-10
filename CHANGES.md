# Changes

## 0.0.4 (2019-XX-XX)

* Fixed #9: Workbenches can be saved even if other plugins contain unnamed UI elements.
* Improved: Handle more cases similar to #7 and #9, which could potentially crash `workbench`.

## 0.0.3 (2019-09-08)

* Implemented #1: Workbenches can be renamed.
* Implemented #2: Workbenches can be imported and exported.
* Implemented #8: Warnings because of unnamed UI elements are turned off by default. If required, they can be activated in the configuration.

## 0.0.2 (2019-09-03)

* Fixed #6: `workbench` does not crash anymore when certain other plugins are loaded. Background: Their UI exposes its Qt parent as a property instead of a method.
* Fixed #7: `workbench` can start even of other plugins contain unnamed UI elements.

## 0.0.1 (2019-09-01)

* Initial release.
