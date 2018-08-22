hlint
=====

Usage
=====

.. code::

   from hlint import lint

   result = lint.check("index.html")
   print(result)
   assert(result.flag == True)

.. code::

   from hlint import lint

   results = lint.check_files(["index.html", "bad.html"])
   print(results)
   assert(results.total_error_count == 1)
