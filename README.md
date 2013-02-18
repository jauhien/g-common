I'm planning to rewrite g-common from here: http://git.overlays.gentoo.org/gitweb/?p=proj/g-cran.git;a=summary

The reason is project is abandoned.

Current status:

- README written ;-)

- first draft

I've created this github repository for my one purposes as a place for documentation/code.
Any information here is for documenting development of this tool.
Any advices are appreciated. )

**g-common** allows you to use non-PMS style repositories in Gentoo

*g-common* implements g-common *layman* interface for overlays.
To use it you should obtain xml file with overlays description and
add it to 'overlays' section in /etc/layman/layman.cfg. Also you
should have appropriate overlay driver installed.
Now if you do layman -L you can find overlays from this xml-file
that have 'g-common' type. Just add them with layman -a.

**g-common interface**

- **g-common** *&lt;overlay&gt;* ***sync*** *&lt;method&gt;* *&lt;url&gt;*

synchronize overlay

*overlay* -- path to overlay

*method* -- type of overlay

*url* -- repository url


- **g-common** *&lt;overlay&gt;* ***generate-tree***

populate overlay with ebuilds and other data

**g-driver interface**

*g-common* uses appropriate *g-driver* to have the job done


- **g-driver** *&lt;overlay&gt;* ***sync*** *&lt;method&gt;* *&lt;url&gt;*

synchronize overlay

*overlay* -- path to overlay

*method* -- type of overlay

*url* -- repository url

- **g-driver** *&lt;overlay&gt;* ***ebuild*** ***list***

list packages from overlay in the format
&lt;category&gt;/&lt;package&gt; &lt;version&gt;
one package per line

- **g-driver** *&lt;overlay&gt;* ***ebuild*** ***src*** &lt;category&gt;/&lt;package&gt; &lt;version&gt;

display source code of a given ebuild

- **g-driver** *&lt;overlay&gt;* ***eclass*** ***list***

list eclasses 

- **g-driver** *&lt;overlay&gt;* ***eclass*** ***src*** &lt;name&gt;

display source code of a given eclass

- **g-driver** *&lt;overlay&gt;* ***license*** ***list***

list eclasses 

- **g-driver** *&lt;overlay&gt;* ***license*** ***src*** &lt;name&gt;

display given license

Every driver should install:
- config file at /usr/share/g-common/drivers/ named &lt;name&gt;.cfg for every overlay-type it supports. An example can be found in https://github.com/jauhien/g-elisp.
- xml-file with list of overlays at /etc/layman/overlays/ (see layman manpage) and https://github.com/jauhien/g-elisp for an example.
