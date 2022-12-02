Distile to version

* ghostscript output is compatible with pdf 1.7
```
 gs \
  -o repaired.pdf \
  -sDEVICE=pdfwrite \
  -dPDFSETTINGS=/prepress \
   corrupted.pdf
```
