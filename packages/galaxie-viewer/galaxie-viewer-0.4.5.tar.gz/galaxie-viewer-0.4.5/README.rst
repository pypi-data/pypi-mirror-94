.. image:: https://readthedocs.org/projects/glxviewer/badge/?version=latest
   :target: https://glxviewer.readthedocs.io/en/latest/?badge=latest
   :alt: Documentation Status
.. image:: https://gitlab.com/Tuuux/galaxie-viewer/badges/master/pipeline.svg
   :target: https://gitlab.com/Tuuux/galaxie-viewer/commits/master
   :alt: Pipeline status
.. image:: https://gitlab.com/Tuuux/galaxie-viewer/badges/master/coverage.svg
   :target: https://gitlab.com/Tuuux/galaxie-viewer/-/commits/master
   :alt: Coverage Status

==============================
Galaxie Viewer's documentation
==============================
.. figure::  https://glxviewer.readthedocs.io/en/latest/_images/logo_galaxie.png
   :align:   center

Description
-----------
Provide a Text Based line viewer, it use a template. It existe many template for high level language, but nothing for text one.

Our mission is to provide useful display template for terminal. Actually every Galaxie tool use it; where print() is not use any more...

Links
-----
  * GitLab: https://gitlab.com/Tuuux/galaxie-viewer/
  * Read the Doc: https://glxviewer.readthedocs.io/
  * PyPI: https://pypi.org/project/galaxie-viewer/
  * PyPI Test: https://test.pypi.org/project/galaxie-viewer/


Screenshots
-----------
v 0.4

.. figure::  https://glxviewer.readthedocs.io/en/latest/_images/screen_01.png
   :align:   center

Installation via pip
--------------------
Pypi

.. code:: bash

  pip install galaxie-viewer

Pypi Test

.. code:: bash

  pip install -i https://test.pypi.org/simple/ galaxie-viewer

Exemple
-------

.. code:: python

  import sys
  import time
  from glxviewer import viewer


  def main():
      start_time = time.time()
      viewer.flush_infos(
          column_1=__file__,
          column_2='Yes that is possible'
      )
      viewer.flush_infos(
          column_1=__file__,
          column_2='it have no difficulty to make it',
          column_3='what ?'
      )
      viewer.flush_infos(
          column_1='Use you keyboard with Ctrl + c for stop the demo',
          status_text='INFO',
          status_text_color='YELLOW',
          status_symbol='!',
      )
      while True:

          viewer.flush_infos(
              column_1=__file__,
              column_2=str(time.time() - start_time),
              status_text='REC',
              status_text_color='RED',
              status_symbol='<',
              prompt=True
          )


  if __name__ == '__main__':
      try:
          main()
      except KeyboardInterrupt:
          viewer.flush_a_new_line()
          sys.exit()

