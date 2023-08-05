.. image:: https://readthedocs.org/projects/galaxie-audio/badge/?version=latest
   :target: https://galaxie-audio.readthedocs.io/en/latest/?badge=latest
   :alt: Documentation Status
.. image:: https://gitlab.com/Tuuux/galaxie-audio/badges/master/pipeline.svg
   :target: https://gitlab.com/Tuuux/galaxie-audio/-/commits/master
   :alt: Pipeline Status
.. image:: https://gitlab.com/Tuuux/galaxie-audio/badges/master/coverage.svg
   :target: https://gitlab.com/Tuuux/galaxie-audio/-/commits/master
   :alt: Coverage Status

===========================
Galaxie Audio documentation
===========================
.. figure:: https://galaxie-audio.readthedocs.io/en/latest/_images/logo_galaxie.png
   :align:  center

Description
-----------
A small Audio library, use by Galaxie Tools for play and record audio.

Links
-----
 * GitLab: https://gitlab.com/Tuuux/galaxie-audio/
 * Read the Doc: https://galaxie-audio.readthedocs.io
 * PyPI: https://pypi.org/project/galaxie-audio/
 * PyPI Test: https://test.pypi.org/project/galaxie-audio/


Screenshots
-----------
v 0.2

.. figure::  https://galaxie-audio.readthedocs.io/en/latest/_images/screen_01.png
   :align:   center

Text Spectrogram

.. figure::  https://galaxie-audio.readthedocs.io/en/latest/_images/screen_02.png
   :align:   center

Installation via pip
--------------------
Pypi

.. code:: bash

  pip install galaxie-audio

Pypi Test

.. code:: bash

  pip install -i https://test.pypi.org/simple/ galaxie-audio

Exemple
-------
.. code:: python

  # Require when you haven't GLXRadio as default Package
  current_dir = os.path.dirname(os.path.abspath(__file__))
  sys.path.append(os.path.dirname(current_dir))

  from glxaudio.AudioRecorder import AudioRecorder
  from glxaudio.AudioPlayer import AudioPLayer
  from glxaudio.AudioInterfaces import AudioInterfaces
  from glxaudio.AudioConstants import GLXAUDIO
  from glxaudio.Sleep import Sleep
  from glxviewer import viewer

  # THE APP
  try:
      verbose = True
      debug = True
      debug_level = 3

      time_to_sleep = 0.42

      if verbose:
          viewer.flush_infos(
              status_text='INIT',
              status_text_color='WHITE',
              column_1='Simplex Repeater',
              column_2=' - Version 0.5'
          )

          viewer.flush_infos(
              status_text='INIT',
              status_text_color='WHITE',
              column_1=AudioInterfaces.__name__ + ':',
              column_2='list interfaces'
          )
          AudioInterfaces.print_interfaces(only_default=True)

      while True:
          #  Create a new temporary file each time, that because communication's should be anonyme
          temporary_file = tempfile.NamedTemporaryFile()
          try:
              # Start a recording
              with AudioRecorder() as recorder:
                  recorder.set_debug(debug)
                  recorder.set_debug_level(debug_level)
                  recorder.set_verbose(verbose)
                  recorder.set_format(GLXAUDIO.FORMAT_INT16)
                  recorder.set_threshold(2)  # in percent
                  recorder.set_channels(1)
                  recorder.set_rate(22050)
                  recorder.set_chunk_size(1024)
                  recorder.record_to_file(filename=temporary_file.name)

              # Wait , because that is how work a repeater
              with Sleep() as sleeper:
                  sleeper.set_debug(debug)
                  sleeper.set_debug_level(debug_level)
                  sleeper.set_verbose(verbose)
                  sleeper.sleep(time_to_sleep)

              # Play what is inside our temporary file
              with AudioPLayer() as player:
                  player.set_debug(debug)
                  player.set_debug_level(debug_level)
                  player.set_verbose(verbose)
                  player.set_is_detached(False)
                  player.play(filename=temporary_file.name)

          except EOFError:
              pass

          # Close the temporary file, it have effect to delete the file.
          # That because communication's should be anonymize
          temporary_file.close()

  except KeyboardInterrupt:
      sys.exit(0)

