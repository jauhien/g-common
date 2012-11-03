I'm planning to rewrite g-common from here: http://git.overlays.gentoo.org/gitweb/?p=proj/g-cran.git;a=summary

The reason is project seems to be abandoned and currently is broken.

Current status:

- README written ;-)

- experiments on getting it working, comming soon )

I've created this github repository for my one purposes as a place for documentation/code.
Any information here is for documenting development of this tool. There is nothing working currently.
Any advices are appreciated. )

**g-common** allows you to use non-PMS style repositories in Gentoo

*g-common* implements g-common *layman* interface for overlays.
To use it you should obtain xml file with overlays description and
add it to 'overlays' section in /etc/layman/layman.cfg. Also you
should have appropriate overlay driver installed.
Now if you do layman -L you can find overlays from this xml-file
that have 'g-common' type. Just add them with layman -a.

**g-common interface**

- **g-common** *&lt;overlay&gt;* ***sync*** *&lt;url&gt;*

synchronize overlay

*overlay* -- path to overlay

*url* -- repository url

- **g-common** *&lt;overlay&gt;* ***generate-tree***

populate overlay with ebuilds and other data

**g-driver interface**

*g-common* uses appropriate *g-driver* to have the job done

- **g-driver** *&lt;overlay&gt;* ***sync*** *&lt;url&gt;*

synchronize overlay

*overlay* -- path to overlay

*url* -- repository url

- **g-driver** *&lt;overlay&gt;* ***list-packages***

list packages from overlay in the format
&lt;category&gt;/&lt;package&gt; &lt;version&gt;
one package per line

- **g-driver** *&lt;overlay&gt;* ***list-categories***

list categories from overlay

- **g-driver** *&lt;overlay&gt;* ***package*** *&lt;category&gt;/&lt;package&gt;* *&lt;version&gt;* *[&lt;var&gt;]*

list variables for given package

If *var* argument is given *g-driver* should print value for this variable or None if it is not set

If *var* is not given *g-driver* should print a list of variables (one per line) in form
&lt;variable name&gt; = &lt;value&gt;

Variables are those that must be set in ebuild,
*GAPI* (API of *g-driver*, currently 0) and *GCOMMON_PHASES* (ebuild function that *g-driver* will handle)

Obligatory variables are: *GAPI*, *EAPI*, *SRC_URI*, *GCOMMON_PHASES*

- **g-driver** *&lt;overlay&gt;* ***phase*** *&lt;category&gt;/&lt;package&gt;* *&lt;version&gt;* *&lt;ebuild-function&gt;*

print source code for a given ebuild function

*g-driver* should print source code only for functions previously returned by *package* command, for other functions it can print just new line or nothing

- **g-driver** ***ebuild*** *&lt;ebuild-function&gt;*

handle given ebuild function, env variables must be set appropriately
