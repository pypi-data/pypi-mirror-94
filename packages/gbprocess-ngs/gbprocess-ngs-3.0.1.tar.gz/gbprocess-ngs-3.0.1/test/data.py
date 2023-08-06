from textwrap import dedent
from gbprocess.operations.operation import Operation

def invalid_fastq_content():
    result = dedent(
        """
        @EU861894-140/1
        +
        ??CFFF?;HHAH#III#I:IHJIJG#JIJJI?3IIJ0JJ#G3JGHG#I90?HIJG9JEIIBD#C#G@#C=)I@#BHBBCDCD;ACDCB;??CD>#D#:DA
        @EU861894-138/1
        AGAGCGCATCCACATGTGGTCCCCCGCTTCGGGGCAGGTTGCCCACGTGTTACGCGACCGTTCGCCATTAACCAC
        +
        @CCF:#@DHHG?BAJJG0BII#GI8;FJIBFBHGJI>+EC=BECBDCHDEAAD#=E6DDFF=9CD#A#8H@@>#D
        """).strip()
    return result

def fastq_forward():
    result = dedent(
        """
        @EU861894-140/1
        CCGATCTCTCGGCCTGCCCGGGGATCTCAAACNCTGGTAAGCTTCTCCGGTTAGTGACGAATCACTGTACCTGCTCCACCGCTTGTGCGGGCCCTCGTCA
        +
        ??CFFF?;HHAH#III#I:IHJIJG#JIJJI?3IIJ0JJ#G3JGHG#I90?HIJG9JEIIBD#C#G@#C=)I@#BHBBCDCD;ACDCB;??CD>#D#:DA
        @EU861894-138/1
        AGAGCGCATCCACATGTGGTCCCCCGCTTCGGGGCAGGTTGCCCACGTGTTACGCGACCGTTCGCCATTAACCAC
        +
        @CCF:#@DHHG?BAJJG0BII#GI8;FJIBFBHGJI>+EC=BECBDCHDEAAD#=E6DDFF=9CD#A#8H@@>#D
        """).strip()
    return result

def fastq_reverse():
    result = dedent(
        """
        @EU861894-140/2
        AGTGAATTGACAGGGGCACGCATAAGCGGTGCGGTATGTGCATTAATTCGTCACTAACTGAAGAACCTCACCAGGCTTTGAAACCCACGGAGAGCGGGAG
        +
        @1@F1FFEFFA#AGGJB!EHDI434:J?GJI##B#)BJIICJJGEBFIBJ>GGDJIGI#)II<H6=ID#E?CD4##CDEFB#C#CA#-<#?#FCE#!DC'
        @EU861894-138/2
        CTTCGGGGGTGGTTAGGCAACCCCCCCCGAAGCGGGGGACAACAGCCTTAAACGGTTCCTAATACCGCATGGTGA
        +
        BB@FB2@FHB2HFJGFFHJ?8=##JDGHDEIBH?H#HI)EFFEF#C#B#HE?#D?#;#DDCA#:DD>BCB###D'
        """).strip()
    return result

def fastq_forward_no_at():
    result = dedent(
        """\
        @EU861894-140/1
        CCGATCTCTCGGCCTGCCCGGGGATCTCAAACNCTGGTAAGCTTCTCCGGTTAGTGACGAATCACTGTACCTGCTCCACCGCTTGCTCCCGCTCTCCGTG
        +
        ??CFFF?;HHAH#III#I:IHJIJG#JIJJI?3IIJ0JJ#G3JGHG#I90?HIJG9JEIIBD#C#G@#C=)I@#BHBBCDCD;ACDCB;??CD>#D#:DA
        @EU861894-138/1
        AGAGCGCATCCACATGTGGTCCCCCGCTTCGGGGCAGGTTGCCCACGTGTTACGCGACCGTTCGCCATTAACCAC
        +
        FCCF:#@DHHG?BAJJG0BII#GI8;FJIBFBHGJI>+EC=BECBDCHDEAAD#=E6DDFF=9CD#A#8H@@>#D
        
        """)
    return result

def fastq_reverse_no_at():
    result = dedent(
        """\
        @EU861894-140/2
        AAGGAATTGACAGGGGCACGCATAAGCGGTGCGGTATGTGCATTAATTCGTCACTAACTGAAGAACCTCACCAGGCTTTGAAACCCACGGAGAGCGGGAG
        +
        F1@F1FFEFFA#AGGJB!EHDI434:J?GJI##B#)BJIICJJGEBFIBJ>GGDJIGI#)II<H6=ID#E?CD4##CDEFB#C#CA#-<#?#FCE#!DC'
        @EU861894-138/2
        CTTCGGGGGTGGTTAGGCAACCCCCCCCGAAGCGGGGGACAACAGCCTTAAACGGTTCCTAATACCGCATGGTGA
        +
        BB@FB2@FHB2HFJGFFHJ?8=##JDGHDEIBH?H#HI)EFFEF#C#B#HE?#D?#;#DDCA#:DD>BCB###DF
        
        """)
    return result

def barcodes():
    result = dedent(
        """
        >barcode1
        CCGAT
        >barcode2
        AGAGC
        """).strip()
    return result

def empty_barcode():
    result = dedent(
        """
        >barcode1
        CCGAT
        >barcode2
        AGAGC
        >

        """).strip()
    return result

def config_only_general_section(input_directory, input_file_name_template, sequencing_type='se', cores=1):
    result = dedent(
        f"""
        [General]
        cores = {cores}
        input_directory = {input_directory}
        sequencing_type = {sequencing_type}
        input_file_name_template = {input_file_name_template}
        """).strip()
    return result

def config_duplicate(input_directory, output_dir, input_file_name_template, sequencing_type='se', unique=""):
    result = dedent(
        f"""
        [General]
        cores = 1
        input_directory = {input_directory}
        sequencing_type = {sequencing_type}
        input_file_name_template = {input_file_name_template}
        
        [MaxNFilter]
        max_n = 0
        output_directory = {output_dir}/01_max_n_filter
        output_file_name_template = {{run}}{{extension}}
        
        [MaxNFilter{unique}]
        max_n = 0
        output_directory = {output_dir}/02_max_n_filter
        output_file_name_template = {{run}}{{extension}}
        """).strip()
    return result