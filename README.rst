rqr - Reading Question Renderer
===============================

Moodle_ quizzes are a great way to ask pre-lecture reading questions, but they lack a good interface for the instructor to read student responses and reply by email. This python module implements a renderer for reading question responses (akin to the one built in to platforms like ILT_).

.. _Moodle: https://moodle.org
.. _ILT: https://galileo.seas.harvard.edu/login/

Usage
-----

In Moodle, use an ungraded quiz to ask reading questions (usually via essay or multichoice questions). After students have responded, do the following:

    - In the instructor view, click "backup".
    - Click "Jump to final step".
    - Click to download the ``.mbz`` file that is made.

Then, on the command line, do ``rqr filename.mbz`` to generate ``filename.html``.

Open this file in your browser to print it or read responses. Click any student's name to respond by email, and their response will be quoted in the message body.


