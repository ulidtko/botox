# http://www.skyfree.org/linux/references/ELF_Format.pdf
# https://www.uclibc.org/docs/elf-64-gen.pdf
import os
import struct

class Elf_Shdr_Flags(object):
    '''
    Convenience wrapper class for reading and writing a section header's flags.
    '''

    def __init__(self, shdr):
        '''
        Class constructor.

        @shdr - Instance of Elf_Shdr.

        Returns None.
        '''
        self.shdr = shdr

    @property
    def write(self):
        if (1 & self.shdr.sh_flags):
            return True
        return False
    @write.setter
    def write(self, value):
        if value == True:
            self.shdr.sh_flags |= 1
        else:
            self.shdr.sh_flags &= ~1

    @property
    def allocate(self):
        if (2 & self.shdr.sh_flags):
            return True
        return False
    @allocate.setter
    def allocate(self, value):
        if value == True:
            self.shdr.sh_flags |= 2
        else:
            self.shdr.sh_flags &= ~2

    @property
    def execute(self):
        if (4 & self.shdr.sh_flags):
            return True
        return False
    @execute.setter
    def execute(self, value):
        if value == True:
            self.shdr.sh_flags |= 4
        else:
            self.shdr.sh_flags &= ~4

class Elf_Shdr(object):
    '''
    Class for reading/writing the contents of an ELF section header entry.
    '''

    def __init__(self, elf, n=0):
        '''
        Class constructor.

        @elf - Instance of the ELF class.
        @n   - The index number of the section header (zero-indexed).

        Returns None.
        '''
        self.elf = elf
        self.index = n

        if self.elf.header.e_shstrndx != self.index:
            self._name = ".shstrtab"
        else:
            self._name = None

        self.flags = Elf_Shdr_Flags(self)

    @property
    def name(self):
        if self.index != self.elf.header.e_shstrndx:
            return self.elf.read_string(self.elf.shstrtab.sh_offset + self.sh_name)
        else:
            return self._name
    @name.setter
    def name(self, value):
        if self.index != self.elf.header.e_shstrndx:
            current_name = self.name
            if len(current_name) > len(value):
                raise Exception("New section header name must be of equal of lesser length than the current name (%s)!" % current_name)
            else:
                self.elf.write_string(self.elf.shstrtab.sh_offset + self.sh_name, value)
        else:
            self._name = value

    @property
    def sh_name(self):
        return self.elf.read_word(self.elf.header.e_shoff+(self.elf.header.e_shentsize*self.index)+0)
    @sh_name.setter
    def sh_name(self, value):
        self.elf.write_word(self.elf.header.e_shoff+(self.elf.header.e_shentsize*self.index)+0, value)

    @property
    def sh_type(self):
        return self.elf.read_word(self.elf.header.e_shoff+(self.elf.header.e_shentsize*self.index)+4)
    @sh_type.setter
    def sh_type(self, value):
        self.elf.write_word(self.elf.header.e_shoff+(self.elf.header.e_shentsize*self.index)+4, value)

    @property
    def sh_flags(self):
        if self.elf.ELFCLASS64 == self.elf.header.e_ident.ei_class:
            return self.elf.read_double(self.elf.header.e_shoff+(self.elf.header.e_shentsize*self.index)+8)
        else:
            return self.elf.read_word(self.elf.header.e_shoff+(self.elf.header.e_shentsize*self.index)+8)
    @sh_flags.setter
    def sh_flags(self, value):
        if self.elf.ELFCLASS64 == self.elf.header.e_ident.ei_class:
            self.elf.write_double(self.elf.header.e_shoff+(self.elf.header.e_shentsize*self.index)+8, value)
        else:
            self.elf.write_word(self.elf.header.e_shoff+(self.elf.header.e_shentsize*self.index)+8, value)

    @property
    def sh_addr(self):
        if self.elf.ELFCLASS64 == self.elf.header.e_ident.ei_class:
            return self.elf.read_double(self.elf.header.e_shoff+(self.elf.header.e_shentsize*self.index)+16)
        else:
            return self.elf.read_word(self.elf.header.e_shoff+(self.elf.header.e_shentsize*self.index)+12)
    @sh_addr.setter
    def sh_addr(self, value):
        if self.elf.ELFCLASS64 == self.elf.header.e_ident.ei_class:
            self.elf.write_double(self.elf.header.e_shoff+(self.elf.header.e_shentsize*self.index)+16, value)
        else:
            self.elf.write_word(self.elf.header.e_shoff+(self.elf.header.e_shentsize*self.index)+12, value)

    @property
    def sh_offset(self):
        if self.elf.ELFCLASS64 == self.elf.header.e_ident.ei_class:
            return self.elf.read_double(self.elf.header.e_shoff+(self.elf.header.e_shentsize*self.index)+24)
        else:
            return self.elf.read_word(self.elf.header.e_shoff+(self.elf.header.e_shentsize*self.index)+16)
    @sh_offset.setter
    def sh_offset(self, value):
        if self.elf.ELFCLASS64 == self.elf.header.e_ident.ei_class:
            self.elf.write_double(self.elf.header.e_shoff+(self.elf.header.e_shentsize*self.index)+24, value)
        else:
            self.elf.write_word(self.elf.header.e_shoff+(self.elf.header.e_shentsize*self.index)+16, value)

    @property
    def sh_size(self):
        if self.elf.ELFCLASS64 == self.elf.header.e_ident.ei_class:
            return self.elf.read_double(self.elf.header.e_shoff+(self.elf.header.e_shentsize*self.index)+32)
        else:
            return self.elf.read_word(self.elf.header.e_shoff+(self.elf.header.e_shentsize*self.index)+20)
    @sh_size.setter
    def sh_size(self, value):
        if self.elf.ELFCLASS64 == self.elf.header.e_ident.ei_class:
            self.elf.write_double(self.elf.header.e_shoff+(self.elf.header.e_shentsize*self.index)+32, value)
        else:
            self.elf.write_word(self.elf.header.e_shoff+(self.elf.header.e_shentsize*self.index)+20, value)

    @property
    def sh_link(self):
        if self.elf.ELFCLASS64 == self.elf.header.e_ident.ei_class:
            return self.elf.read_word(self.elf.header.e_shoff+(self.elf.header.e_shentsize*self.index)+40)
        else:
            return self.elf.read_word(self.elf.header.e_shoff+(self.elf.header.e_shentsize*self.index)+24)
    @sh_link.setter
    def sh_link(self, value):
        if self.elf.ELFCLASS64 == self.elf.header.e_ident.ei_class:
            self.elf.write_word(self.elf.header.e_shoff+(self.elf.header.e_shentsize*self.index)+40, value)
        else:
            self.elf.write_word(self.elf.header.e_shoff+(self.elf.header.e_shentsize*self.index)+24, value)

    @property
    def sh_info(self):
        if self.elf.ELFCLASS64 == self.elf.header.e_ident.ei_class:
            return self.elf.read_word(self.elf.header.e_shoff+(self.elf.header.e_shentsize*self.index)+44)
        else:
            return self.elf.read_word(self.elf.header.e_shoff+(self.elf.header.e_shentsize*self.index)+28)
    @sh_info.setter
    def sh_info(self, value):
        if self.elf.ELFCLASS64 == self.elf.header.e_ident.ei_class:
            self.elf.write_word(self.elf.header.e_shoff+(self.elf.header.e_shentsize*self.index)+44, value)
        else:
            self.elf.write_word(self.elf.header.e_shoff+(self.elf.header.e_shentsize*self.index)+28, value)

    @property
    def sh_addralign(self):
        if self.elf.ELFCLASS64 == self.elf.header.e_ident.ei_class:
            return self.elf.read_double(self.elf.header.e_shoff+(self.elf.header.e_shentsize*self.index)+48)
        else:
            return self.elf.read_word(self.elf.header.e_shoff+(self.elf.header.e_shentsize*self.index)+32)
    @sh_addralign.setter
    def sh_addralign(self, value):
        if self.elf.ELFCLASS64 == self.elf.header.e_ident.ei_class:
            self.elf.write_double(self.elf.header.e_shoff+(self.elf.header.e_shentsize*self.index)+48, value)
        else:
            self.elf.write_word(self.elf.header.e_shoff+(self.elf.header.e_shentsize*self.index)+32, value)

    @property
    def sh_entsize(self):
        if self.elf.ELFCLASS64 == self.elf.header.e_ident.ei_class:
            return self.elf.read_double(self.elf.header.e_shoff+(self.elf.header.e_shentsize*self.index)+56)
        else:
            return self.elf.read_word(self.elf.header.e_shoff+(self.elf.header.e_shentsize*self.index)+36)
    @sh_entsize.setter
    def sh_entsize(self, value):
        if self.elf.ELFCLASS64 == self.elf.header.e_ident.ei_class:
            self.elf.write_double(self.elf.header.e_shoff+(self.elf.header.e_shentsize*self.index)+56, value)
        else:
            self.elf.write_word(self.elf.header.e_shoff+(self.elf.header.e_shentsize*self.index)+36, value)

class Elf_Phdr_Flags(object):
    '''
    Convenience wrapper class for reading and writing a program header's flags.
    '''

    def __init__(self, phdr):
        '''
        Class constructor.

        @phdr - Instance of the ELf32_Phdr class.

        Returns None.
        '''
        self.phdr = phdr

    @property
    def read(self):
        if 0b100 & self.phdr.p_flags:
            return True
        return False
    @read.setter
    def read(self, tf):
        if True == tf:
            self.phdr.p_flags |= 0b100
        else:
            self.phdr.p_flags &= ~0b100

    @property
    def write(self):
        if 0b010 & self.phdr.p_flags:
            return True
        return False
    @write.setter
    def write(self, tf):
        if True == tf:
            self.phdr.p_flags |= 0b010
        else:
            self.phdr.p_flags &= ~0b010

    @property
    def execute(self):
        if 0b001 & self.phdr.p_flags:
            return True
        return False
    @execute.setter
    def execute(self, tf):
        if True == tf:
            self.phdr.p_flags |= 0b001
        else:
            self.phdr.p_flags &= ~0b001

class Elf_Phdr(object):
    '''
    Class for reading/writing the contents of an ELF program header entry.
    '''

    def __init__(self, elf, n=0):
        '''
        Class constructor.

        @elf - An instance of the ELF class.
        @n   - The index number of the program header (zero-indexed).

        Returns None.
        '''
        self.elf = elf
        self.index = n
        self.flags = Elf_Phdr_Flags(self)

    @property
    def p_type(self):
        return self.elf.read_word(self.elf.header.e_phoff+(self.elf.header.e_phentsize*self.index)+0)
    @p_type.setter
    def p_type(self, value):
        self.elf.write_word(self.elf.header.e_phoff+(self.elf.header.e_phentsize*self.index)+0, value)

    @property
    def p_offset(self):
        if self.elf.ELFCLASS64 == self.elf.header.e_ident.ei_class:
            return self.elf.read_double(self.elf.header.e_phoff+(self.elf.header.e_phentsize*self.index)+8)
        else:
            return self.elf.read_word(self.elf.header.e_phoff+(self.elf.header.e_phentsize*self.index)+4)
    @p_offset.setter
    def p_offset(self, value):
        if self.elf.ELFCLASS64 == self.elf.header.e_ident.ei_class:
            self.elf.write_double(self.elf.header.e_phoff+(self.elf.header.e_phentsize*self.index)+8, value)
        else:
            self.elf.write_word(self.elf.header.e_phoff+(self.elf.header.e_phentsize*self.index)+4, value)

    @property
    def p_vaddr(self):
        if self.elf.ELFCLASS64 == self.elf.header.e_ident.ei_class:
            return self.elf.read_double(self.elf.header.e_phoff+(self.elf.header.e_phentsize*self.index)+16)
        else:
            return self.elf.read_word(self.elf.header.e_phoff+(self.elf.header.e_phentsize*self.index)+8)
    @p_vaddr.setter
    def p_vaddr(self, value):
        if self.elf.ELFCLASS64 == self.elf.header.e_ident.ei_class:
            self.elf.write_double(self.elf.header.e_phoff+(self.elf.header.e_phentsize*self.index)+16, value)
        else:
            self.elf.write_word(self.elf.header.e_phoff+(self.elf.header.e_phentsize*self.index)+8, value)

    @property
    def p_paddr(self):
        if self.elf.ELFCLASS64 == self.elf.header.e_ident.ei_class:
            return self.elf.read_double(self.elf.header.e_phoff+(self.elf.header.e_phentsize*self.index)+24)
        else:
            return self.elf.read_word(self.elf.header.e_phoff+(self.elf.header.e_phentsize*self.index)+12)
    @p_paddr.setter
    def p_paddr(self, value):
        if self.elf.ELFCLASS64 == self.elf.header.e_ident.ei_class:
            self.elf.write_double(self.elf.header.e_phoff+(self.elf.header.e_phentsize*self.index)+24, value)
        else:
            self.elf.write_word(self.elf.header.e_phoff+(self.elf.header.e_phentsize*self.index)+12, value)

    @property
    def p_filesz(self):
        if self.elf.ELFCLASS64 == self.elf.header.e_ident.ei_class:
            return self.elf.read_double(self.elf.header.e_phoff+(self.elf.header.e_phentsize*self.index)+32)
        else:
            return self.elf.read_word(self.elf.header.e_phoff+(self.elf.header.e_phentsize*self.index)+16)
    @p_filesz.setter
    def p_filesz(self, value):
        if self.elf.ELFCLASS64 == self.elf.header.e_ident.ei_class:
            self.elf.write_double(self.elf.header.e_phoff+(self.elf.header.e_phentsize*self.index)+32, value)
        else:
            self.elf.write_word(self.elf.header.e_phoff+(self.elf.header.e_phentsize*self.index)+16, value)

    @property
    def p_memsz(self):
        if self.elf.ELFCLASS64 == self.elf.header.e_ident.ei_class:
            return self.elf.read_double(self.elf.header.e_phoff+(self.elf.header.e_phentsize*self.index)+40)
        else:
            return self.elf.read_word(self.elf.header.e_phoff+(self.elf.header.e_phentsize*self.index)+20)
    @p_memsz.setter
    def p_memsz(self, value):
        if self.elf.ELFCLASS64 == self.elf.header.e_ident.ei_class:
            self.elf.write_double(self.elf.header.e_phoff+(self.elf.header.e_phentsize*self.index)+40, value)
        else:
            self.elf.write_word(self.elf.header.e_phoff+(self.elf.header.e_phentsize*self.index)+20, value)

    @property
    def p_flags(self):
        if self.elf.ELFCLASS64 == self.elf.header.e_ident.ei_class:
            return self.elf.read_word(self.elf.header.e_phoff+(self.elf.header.e_phentsize*self.index)+4)
        else:
            return self.elf.read_word(self.elf.header.e_phoff+(self.elf.header.e_phentsize*self.index)+24)
    @p_flags.setter
    def p_flags(self, value):
        if self.elf.ELFCLASS64 == self.elf.header.e_ident.ei_class:
            self.elf.write_word(self.elf.header.e_phoff+(self.elf.header.e_phentsize*self.index)+4, value)
        else:
            self.elf.write_word(self.elf.header.e_phoff+(self.elf.header.e_phentsize*self.index)+24, value)

    @property
    def p_align(self):
        if self.elf.ELFCLASS64 == self.elf.header.e_ident.ei_class:
            return self.elf.read_double(self.elf.header.e_phoff+(self.elf.header.e_phentsize*self.index)+48)
        else:
            return self.elf.read_word(self.elf.header.e_phoff+(self.elf.header.e_phentsize*self.index)+28)
    @p_align.setter
    def p_align(self, value):
        if self.elf.ELFCLASS64 == self.elf.header.e_ident.ei_class:
            self.elf.write_double(self.elf.header.e_phoff+(self.elf.header.e_phentsize*self.index)+48, value)
        else:
            self.elf.write_word(self.elf.header.e_phoff+(self.elf.header.e_phentsize*self.index)+28, value)

class Elf_Ident(object):
    '''
    Class for reading/writing the contents of the e_ident section of the ELF header.
    '''

    def __init__(self, elf):
        '''
        Class constructor.

        @elf - An instance of the ELF class.

        Returns None.
        '''
        self.elf = elf

    @property
    def ei_magic(self):
        return self.elf.read(0, 4)
    @ei_magic.setter
    def ei_magic(self, value):
        self.elf.write(0, value[0:3])

    @property
    def ei_class(self):
        return self.elf.read_byte(4)
    @ei_class.setter
    def ei_class(self, value):
        self.elf.write_byte(4, value)

    @property
    def ei_encoding(self):
        return self.elf.read_byte(5)
    @ei_encoding.setter
    def ei_encoding(self, value):
        return self.elf.write_byte(5, value)

    @property
    def ei_version(self):
        return self.elf.read_byte(6)
    @ei_version.setter
    def ei_version(self, value):
        return self.elf.write_byte(6, value)

class Elf_Header(object):
    '''
    Class for reading/writing the contents of an ELF header.
    '''

    def __init__(self, elf):
        '''
        Class constructor.

        @elf - An instance of the ELF class.

        Returns None.
        '''
        self.elf = elf
        self.e_ident = Elf_Ident(self.elf)

    @property
    def e_type(self):
        return self.elf.read_half(16)
    @e_type.setter
    def e_type(self, value):
        self.elf.write_half(16, value)

    @property
    def e_machine(self):
        return self.elf.read_half(18)
    @e_machine.setter
    def e_machine(self, value):
        self.elf.write_half(18, value)

    @property
    def e_version(self):
        return self.elf.read_word(20)
    @e_version.setter
    def e_version(self, value):
        self.elf.write_word(20, value)

    @property
    def e_entry(self):
        if self.elf.ELFCLASS64 == self.e_ident.ei_class:
            return self.elf.read_double(24)
        else:
            return self.elf.read_word(24)
    @e_entry.setter
    def e_entry(self, value):
        if self.elf.ELFCLASS64 == self.e_ident.ei_class:
            self.elf.write_double(24, value)
        else:
            self.elf.write_word(24, value)

    @property
    def e_phoff(self):
        if self.elf.ELFCLASS64 == self.e_ident.ei_class:
            return self.elf.read_double(32)
        else:
            return self.elf.read_word(28)
    @e_phoff.setter
    def e_phoff(self, value):
        if self.elf.ELFCLASS64 == self.e_ident.ei_class:
            self.elf.write_double(32)
        else:
            self.elf.write_word(28, value)

    @property
    def e_shoff(self):
        if self.elf.ELFCLASS64 == self.e_ident.ei_class:
            return self.elf.read_double(40)
        else:
            return self.elf.read_word(32)
    @e_shoff.setter
    def e_shoff(self, value):
        if self.elf.ELFCLASS64 == self.e_ident.ei_class:
            self.elf.write_double(40, value)
        else:
            self.elf.write_word(32, value)

    @property
    def e_flags(self):
        if self.elf.ELFCLASS64 == self.e_ident.ei_class:
            return self.elf_read_word(48)
        else:
            return self.elf.read_word(36)
    @e_flags.setter
    def e_flags(self, value):
        if self.elf.ELFCLASS64 == self.e_ident.ei_class:
            self.elf.write_word(48, value)
        else:
            self.elf.write_word(36, value)

    @property
    def e_ehsize(self):
        if self.elf.ELFCLASS64 == self.e_ident.ei_class:
            return self.elf.read_half(52)
        else:
            return self.elf.read_half(40)
    @e_ehsize.setter
    def e_ehsize(self, value):
        if self.elf.ELFCLASS64 == self.e_ident.ei_class:
            self.elf.write_half(52, value)
        else:
            self.elf.write_half(40, value)

    @property
    def e_phentsize(self):
        if self.elf.ELFCLASS64 == self.e_ident.ei_class:
            return self.elf.read_half(54)
        else:
            return self.elf.read_half(42)
    @e_phentsize.setter
    def e_phentsize(self, value):
        if self.elf.ELFCLASS64 == self.e_ident.ei_class:
            self.elf.write_half(54, value)
        else:
            self.elf.write_half(42, value)

    @property
    def e_phnum(self):
        if self.elf.ELFCLASS64 == self.e_ident.ei_class:
            return self.elf.read_half(56)
        else:
            return self.elf.read_half(44)
    @e_phnum.setter
    def e_phnum(self, value):
        if self.elf.ELFCLASS64 == self.e_ident.ei_class:
            self.elf.write_half(56, value)
        else:
            self.elf.write_half(44, value)

    @property
    def e_shentsize(self):
        if self.elf.ELFCLASS64 == self.e_ident.ei_class:
            return self.elf.read_half(58)
        else:
            return self.elf.read_half(46)
    @e_shentsize.setter
    def e_shentsize(self, value):
        if self.elf.ELFCLASS64 == self.e_ident.ei_class:
            self.elf.write_half(58, value)
        else:
            self.elf.write_half(46, value)

    @property
    def e_shnum(self):
        if self.elf.ELFCLASS64 == self.e_ident.ei_class:
            return self.elf.read_half(60)
        else:
            return self.elf.read_half(48)
    @e_shnum.setter
    def e_shnum(self, value):
        if self.elf.ELFCLASS64 == self.e_ident.ei_class:
            self.elf.write_half(60, value)
        else:
            self.elf.write_half(48, value)

    @property
    def e_shstrndx(self):
        if self.elf.ELFCLASS64 == self.e_ident.ei_class:
            return self.elf.read_half(62)
        else:
            return self.elf.read_half(50)
    @e_shstrndx.setter
    def e_shstrndx(self, value):
        if self.elf.ELFCLASS64 == self.e_ident.ei_class:
            self.elf.write_half(62, value)
        else:
            self.elf.write_half(50, value)

class ELF(object):
    '''
    Primary class for accessing and manipulating ELF files.
    Most other classes consist primarily of setters/getters.

    Important class objects:

        o self.size            - Returns the size of the ELF file on disk
        o self.header          - EL32_Header object, providing access to the ELF header data
        o self.program_headers - List of Elf_Phdr objects, providing access to the program header data
        o self.section_headers - List of Elf_Shdr objects, providing access to the section header data

    Be careful using this class to access elements of the ELF header!! Most everything is implemented
    as getters/setters that directly access the target file on disk. This means, for example, that
    reading from ELF.header.e_entry results in a read from the file, and assigning a value to
    ELF.header.e_entry results in that value being written to the file!

    If you want to make *sure* nothing gets accidentally written to disk, instantiate this class with
    read_only=True.
    '''

    ELFDATA2LSB = 1
    ELFDATA2MSB = 2

    ET_NONE = 0
    ET_REL = 1
    ET_EXEC = 2
    ET_DYN = 3
    ET_CORE = 4
    ET_LOPROC = 0xFF00
    ET_HIPROC = 0xFFFF

    PT_NULL = 0
    PT_LOAD = 1
    PT_DYNAMIC = 2
    PT_INTERP = 3
    PT_NOTE = 4
    PT_SHLIB = 5
    PT_PHDR = 6
    PT_LOOS = 0x60000000
    PT_HIOS = 0x6FFFFFFF
    PT_LOPROC = 0x70000000
    PT_HIPROC = 0x7FFFFFFF

    EM_NONE = 0
    EM_SPARC = 2
    EM_386 = 3
    EM_MIPS = 8
    EM_ARM = 40
    EM_X86_64 = 62

    ELFCLASSNONE = 0
    ELFCLASS32 = 1
    ELFCLASS64 = 2

    SHT_SYMTAB = 2
    SHT_DYNSYM = 11

    def __init__(self, elfile, read_only=False):
        '''
        Class constructor.

        @elfile    - The ELF file to load.
        @read_only - Set to True for read-only access to the file.

        Returns None.
        '''
        self.read_only = read_only

        if self.read_only == True:
            self.file_mode = 'rb'
        else:
            self.file_mode = 'r+b'

        # Get absolute path to the file
        self.elfile = os.path.abspath(elfile)

        # Process the ELF header, along with program and section headers
        self._load_elf_file()

    def __enter__(self):
        return self

    def __exit__(self, t, v, b):
        self.fp.close()
        return None

    def _load_elf_file(self):
        '''
        Opens and loads critical data from the ELF file.

        Returns None.
        '''
        # Open the ELF file
        self._open_file()

        # Create a ELF header object
        self.header = Elf_Header(self)

        # Grab all the program headers
        self.program_headers = []
        for n in range(0, self.header.e_phnum):
            phdr = Elf_Phdr(self, n)
            self.program_headers.append(phdr)

        # Get the strings section header so that subsequent section
        # headers can resolve their section names.
        self.shstrtab = Elf_Shdr(self, self.header.e_shstrndx)

        # Grab all the section headers
        self.section_headers = []
        for n in range(0, self.header.e_shnum):
            shdr = Elf_Shdr(self, n)
            self.section_headers.append(shdr)

    # The below methods are the only ones that should touch self.fp
    # directly! All others should be wrappers around these.
    def _open_file(self):
        '''
        Opens the ELF file whose path is listed in self.elfile.

        Returns None.
        '''
        # Open the file in unbuffered mode
        self.fp = open(self.elfile, self.file_mode, 0)
    def _read_from_file(self, offset, size):
        '''
        Read data from the ELF file.

        @offset - Seek to this file offset before reading
        @size   - Number of bytes to read

        Returns a string of data read from the file.
        '''
        self.fp.seek(offset)
        return self.fp.read(size)
    def _write_to_file(self, offset, data):
        '''
        Write data to the ELF file.

        @offset - Seek to this file offset before writing
        @data   - Data to write to the file

        Returns None.
        '''
        self.fp.seek(offset)
        self.fp.write(data)
        # Shouldn't need the flush since the file is opened
        # in unbuffered mode, but it can't hurt...right??
        self.fp.flush()
    def _file_overwrite(self, data):
        '''
        Completely overwrite and re-load the ELF file on disk.

        @data - Overwrite the ELF file with this data.
                If in read-only mode, nothing will happen.

        Returns None.
        '''
        # TODO: Should raise an exception if self.read_only is True?
        if self.read_only == False:
            self.fp.close()
            fp = open(self.elfile, "wb")
            fp.write(data)
            fp.close()
            self._load_elf_file()
    @property
    def size(self):
        self.fp.seek(0, 2)
        return self.fp.tell()
    @size.setter
    def size(self):
        return None
    # End of methods that should be directly accessing self.fp!

    # These two methods are the only ones that should be accessing
    # the internal _read_from_file and _write_to_file methods!
    def read(self, offset, size):
        return self._read_from_file(offset, size)
    def write(self, offset, data):
        return self._write_to_file(offset, data)

    # These three methods are the only ones that should be accessing
    # the internal _file_overwrite method!
    def insert(self, offset, data):
        '''
        Insert data into the ELF file.

        @offset - Seek to this file offset before writing.
        @data   - Insert this data to file.

        Returns None.
        '''
        elf_file_contents = self.read(0, offset)
        elf_file_contents += data
        elf_file_contents += self.read(offset, (self.size-offset))
        self._file_overwrite(elf_file_contents)
    def append(self, data):
        '''
        Append data to the end of the ELF file.

        @data - Data to append.

        Returns None.
        '''
        elf_file_contents = self.read(0, self.size)
        elf_file_contents += data
        self.write(0, elf_file_contents)
        self._file_overwrite(elf_file_contents)
    def delete(self, offset, size):
        '''
        Remove data from the ELF file.

        @offset - Seek to this file offset before deleting.
        @size   - Delete this many bytes from the file.

        Returns None.
        '''
        elf_file_contents = self.read(0, offset)
        elf_file_contents += self.read((offset+size), (self.size - (offset+size)))
        self._file_overwrite(elf_file_contents)

    def write_string(self, offset, data):
        '''
        Write data to the ELF file, adding a NULL terminating character.

        @offset - Seek to this file offset before writing.
        @data   - Write this data to file.

        Returns None.
        '''
        return self.write(offset, data + "\x00")

    def read_string(self, offset, size=None):
        '''
        Read a string of data from the ELF file.

        @offset - Seek to this file offset before reading.
        @size   - Number of bytes to read.
                  If None, this will read up to, but not including, the first NULL byte.

        Returns the data read from the file.
        '''
        # Read in blocks of 1024. Better for disk I/O than doing one byte at a time.
        block_size = 1024
        i = 0
        data = ""

        if size is None:
            while True:
                chunk = self.read(offset+i, block_size)
                if b"\x00" in chunk:
                    data += chunk.split(b"\x00")[0]
                    break
                elif not chunk:
                    break
                else:
                    data += chunk
                    i += block_size
        else:
            data = self.read(offset, size)

        return data

    @property
    def endianess(self):
        # Before doing anything else, we need to know what endianess the target is
        if self.ELFDATA2MSB == self.header.e_ident.ei_encoding:
            return ">"
        else:
            return "<"
    @endianess.setter
    def endianess(self, value):
        # This really is for internal use to interface with the struct module.
        # You shouldn't be setting it! If you want to modify the ELF file's
        # endianess flag, access it via self.header.e_ident.ei_encoding.
        pass

    def read_byte(self, offset):
        return ord(self.read(offset, 1))
    def write_byte(self, offset, value):
        self.write(offset, chr(value))

    def read_half(self, offset):
        return struct.unpack("%sH" % self.endianess, self.read(offset, 2))[0]
    def write_half(self, offset, value):
        self.write(offset, struct.pack("%sH" % self.endianess, value))

    def read_word(self, offset):
        return struct.unpack("%sL" % self.endianess, self.read(offset, 4))[0]
    def write_word(self, offset, value):
        self.write(offset, struct.pack("%sL" % self.endianess, value))

    def read_double(self, offset):
        return struct.unpack("%sq" % self.endianess, self.read(offset, 8))[0]
    def write_double(self, offset, value):
        self.write(offset, struct.pack("%sq" % self.endianess, value))

    def read_address(self, offset):
        if self.ELFCLASS64 == self.header.e_ident.ei_class:
            return self.read_double(offset)
        else:
            return self.read_word(offset)
    def write_address(self, offset, value):
        if self.ELFCLASS64 == self.header.e_ident.ei_class:
            return self.write_double(offset, value)
        else:
            return self.write_word(offset, value)




