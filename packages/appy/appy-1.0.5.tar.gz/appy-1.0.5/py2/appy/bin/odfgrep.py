'''This script allows to perform a "grep" command that will be applied on files
   content.xml and styles.xml within all ODF files (odt and ods) found within a
   given folder.'''

# ------------------------------------------------------------------------------
import re, sys, os.path, StringIO

from appy import Object as O
from appy.shared.zip import zip, unzip
from appy.shared import utils as sutils

# ------------------------------------------------------------------------------
ZONE_KO   = 'The single valid value for "zone" is "pod".'

# ------------------------------------------------------------------------------
usage = '''Usage: python odfgrep.py keyword file|folder [repl] [zone].

 *keyword* is the string or regular expression to search within the file(s).

 If *file* is given, it is the path to an ODF file (odt or ods). grep will be
 run on this file only.

 If *folder* is given, the grep will be run on all ODF files found in this
 folder and sub-folders.

 If *repl* is given, within matched ODF files, *keyword* will be replaced with
 *repl*.

 If *zone* is "pod", replacements will be performed in "pod" zones only (notes,
 fields) and not anywhere in the files.
'''

# ------------------------------------------------------------------------------
class Grep:
    toGrep = ('content.xml', 'styles.xml')
    toUnzip = ('.ods', '.odt')

    # Messages ~{ b_replace: { b_match: s_message }}~
    messageTexts = { True:  {True:  '%s: %d replacement(s) done.',
                             False: 'No replacement was made.'},
                     False: {True:  '%s matches %d time(s).',
                             False: 'No match found.'}}

    # ODF tags used by POD statements or expressions
    podTags = ('office:annotation', 'text:conditional-text', 'text:text-input')

    def __init__(self, keyword, fileOrFolder, repl=None, zone=None,
                 onFileChanged=False):
        # Create a regex from the passed p_keyword
        self.keyword = re.compile(keyword, re.S)
        # The file or folder where to find POD templates
        self.fileOrFolder = fileOrFolder
        # A temp folder where to unzip the POD templates
        self.tempFolder = sutils.getOsTempFolder()
        # (optional) The replacement text
        self.repl = repl
        # (optional) The replacement zone
        self.zoneRex = self.getZoneRex(zone)
        # If called from another program (ie class RamGrep below),
        # p_onFileChanged is a function that will be called every time a file
        # will be modified by this class, with the absolute file name as single
        # argument.
        self.onFileChanged = onFileChanged
        # If called programmatically, we don't want any output on stdout
        self.silent = bool(onFileChanged)
        if self.silent:
            self.messages = []

    def getZoneRex(self, zone):
        '''Return the regex representing pod zones within content|styles.xml.
           If no p_zone is passed, return None.'''
        if not zone: return
        elif zone != 'pod':
            raise Exception(ZONE_KO)
        else:
            # Build the regex
            tags = []
            for tag in self.podTags:
                tags.append('(?:%s)' % tag)
            tags = '|'.join(tags)
            return re.compile('<(?P<tag>%s)(.*?)</(?P=tag)>' % tags, re.S)

    def dump(self, message):
        '''Dumps a p_message, either on stdout or in self.messages if we run in
           silent mode.'''
        if self.silent:
            self.messages.append(message)
        else:
            print(message)

    def getMessage(self):
        '''Returns self.messages, concatenated in a single string'''
        messages = getattr(self, 'messages', None)
        if not messages: return ''
        return '\n'.join(messages)

    def getReplacement(self):
        '''Return p_self.repl and increment p_self.tempCount'''
        # This method is used to count the number of replacements
        self.tempCount += 1
        return self.repl

    def getZoneReplacement(self, match):
        '''A POD zone has been found in a file, in m_match. Perform replacements
           within this zone.'''
        r = self.keyword.sub(lambda m: self.getReplacement(), match.group(2))
        tag = match.group(1)
        return '<%s%s</%s>' % (tag, r, tag)

    def greplace(self, name, content, tempFolder):
        '''Replace, in file named p_name lying in p_tempFolder and whose content
           is in p_content as a string, every occurrence of p_self.keyword (a
           regex) by p_self.repl. Return the number of replacements
           performed.'''
        # Initialise a temp counter on p_self
        self.tempCount = 0
        # Perform the replacement(s)
        zoneRex = self.zoneRex
        if not zoneRex:
            fun = lambda match: self.getReplacement()
            content = self.keyword.sub(fun, content)
        else:
            # Restrict replacement to zones as defined by p_self.zoneRex
            fun = lambda match: self.getZoneReplacement(match)
            content = zoneRex.sub(fun, content)
        # Overwrite the file if at least one replacement has been performed
        if self.tempCount:
            tempFileName = os.path.join(tempFolder, name)
            f = open(tempFileName, 'w')
            f.write(content)
            f.close()
        return self.tempCount

    def grepFileContent(self, fileName, tempFolder, contents):
        '''Finds self.keyword among p_tempFolder/content.xml and
           p_tempFolder/styles.xml, whose content is in p_contents and was
           extracted from p_fileName, and return the number of matches.

           If self.repl is there, and if there is at least one match, the method
           replaces self.keyword by self.repl for all matches, re-zips the ODF
           file whose parts are in p_tempFolder and overwrites the original file
           in p_fileName.'''
        count = 0
        for name in self.toGrep:
            # Get the file content
            content = contents[name]
            # Are there matches ?
            found = self.keyword.findall(content)
            if not found: continue
            if self.repl:
                # Perform replacements when relevant
                count += self.greplace(name, content, tempFolder)
            else:
                count += len(found)
        # Re-zip the result when relevant
        if count and self.repl:
            zip(fileName, tempFolder, odf=True)
        return count

    def grepFile(self, fileName):
        '''Unzip the .xml files from file named p_fileName and perform a grep on
           it.'''
        # Unzip the file in the temp folder
        tempFolder = sutils.getOsTempFolder(sub=True)
        # Unzip the file in its entirety
        contents = unzip(fileName, tempFolder, odf=True)
        nb = self.grepFileContent(fileName, tempFolder, contents)
        if nb:
            msg = self.messageTexts[bool(self.repl)][bool(nb)] % (fileName, nb)
            self.dump(msg)
            if self.repl and self.onFileChanged:
                self.onFileChanged(fileName)
        # Delete the temp folder
        sutils.FolderDeleter.delete(tempFolder)
        return nb

    def run(self):
        '''Performs the "grep" on self.fileOrFolder. If called by RamGrep, it
           outputs messages on stdout. Else, it dumps it in self.messages.'''
        nb = 0
        if os.path.isfile(self.fileOrFolder):
            nb += self.grepFile(self.fileOrFolder)
        elif os.path.isdir(self.fileOrFolder):
            # Grep on all files found in this folder
            for dir, dirnames, filenames in os.walk(self.fileOrFolder):
                for name in filenames:
                    if os.path.splitext(name)[1] in self.toUnzip:
                        nb += self.grepFile(os.path.join(dir, name))
        else:
            self.dump('%s does not exist.' % self.fileOrFolder)
        if not nb:
            self.dump(self.messageTexts[bool(self.repl)][False])
        return nb

# ------------------------------------------------------------------------------
class RamGrep:
    '''Wrapper around class Grep allowing to use it programmatically, from an
       ODF file given as a StringIO. The result is stored in RamGrep's
       attributes, instead of (a) messages produced on stdout and (b) files
       potentially overwritten on disk in replace mode.'''

    def __init__(self, keyword, stringIo, repl=None, extension='odt'):
        # Create the underlying Grep instance
        self.grep = Grep(keyword, None, repl, onFileChanged=self.onFileChanged)
        # Store the StringIO instance
        self.stringIo = stringIo
        # The file extension corresponding to the file whose content is in
        # p_stringIo must be specified here.
        self.extension = extension
        # After the operation, has the file changed ? It is the case if p_repl
        # is given and if at least one occurrence of p_keyword has been found.
        self.modified = False
        # The messages produced by the operation are concatenated into a single
        # string, hereafter.
        self.message = None
        # If the input file (p_stringIo) has been modified, the modified file
        # will be stored in another StringIO intance, in the following
        # attribute.
        self.result = None

    def onFileChanged(self, fileName):
        '''p_fileName has been modified by self.grep. Store its content as a
           StringIO instance on self.result.'''
        # Get the content of the modified file
        r = StringIO.StringIO()
        f = open(fileName, 'rb')
        content = f.read()
        f.close()
        # Copy this content in the result StringIO instance
        r.write(content)
        self.result = r

    def run(self):
        # Dump self.stringIo in a temp file on disk
        fileName = sutils.getTempFileName('RAMGREP', self.extension)
        f = open(fileName, 'wb')
        content = self.stringIo.getvalue()
        f.write(content)
        f.close()
        # Run the grep
        self.grep.fileOrFolder = fileName
        nb = self.grep.run()
        # Store grep's outputs
        self.modified = bool(self.grep.repl and nb)
        self.message = self.grep.getMessage()
        # Remove the temporary file
        if os.path.exists(fileName):
            os.remove(fileName)

# ------------------------------------------------------------------------------
if __name__ == '__main__':
    if len(sys.argv) not in (3, 4, 5):
        print(usage)
        sys.exit()
    Grep(*sys.argv[1:]).run()
# ------------------------------------------------------------------------------
