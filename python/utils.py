import six


def get_bom_from_string(input_str, input_encoding=None):
    """
                                Byte0    Byte1   Byte2   Byte3   Encoding
        Explicit BOM            #x00 	 #x00 	 #xFE 	 #xFF 	 UTF-32BE
        ASCII first character 	#x00 	 #x00 	 #x00 	 any 	 UTF-32BE
        Explicit BOM 	        #xFF 	 #xFE 	 #x00 	 #x00 	 UTF-32LE
        ASCII first character 	any 	 #x00 	 #x00 	 #x00 	 UTF-32LE
        Explicit BOM 	        #xFE 	 #xFF       	  	  	 UTF-16BE
        ASCII first character 	#x00 	 any 	  	          	 UTF-16BE
        Explicit BOM 	        #xFF 	 #xFE 	  	  	         UTF-16LE
        ASCII first character 	any 	 #x00 	  	  	         UTF-16LE
        Explicit BOM 	        #xEF 	 #xBB 	 #xBF 	  	     UTF-8
        Default 	  	  	    UTF-8
    """
    x00 = ord('\x00')
    xfe = ord('\xFE')
    xff = ord('\xFF')
    xef = ord('\xEF')
    xbb = ord('\xBB')
    xbf = ord('\xBF')

    max_len = min(4, len(input_str))
    if six.PY2:
        sig = [ord(input_str[i]) for i in range(max_len)]
    else:
        if isinstance(input_str, str):
            sig = [ord(input_str[i]) for i in range(max_len)]
        else:
            assert isinstance(input_str, bytes)
            sig = [input_str[i] for i in range(max_len)]

    bom = ''

    if input_encoding is None:
        if len(sig) >= 4 and sig[0] == x00 and sig[1] == x00 and sig[2] == xfe and sig[3] == xff:
            encoding = 'utf-32-be'
            bom = sig[0:4]
        elif len(sig) >= 4 and sig[0] == x00 and sig[1] == x00 and sig[2] == x00:
            encoding = 'utf-32-be'
        elif len(sig) >= 4 and sig[0] == xff and sig[1] == xfe and sig[2] == x00 and sig[3] == x00:
            encoding = 'utf-32-le'
            bom = sig[0:4]
        elif len(sig) >= 2 and sig[1] == x00 and sig[2] == x00 and sig[3] == x00:
            encoding = 'utf-32-le'
        elif len(sig) >= 2 and sig[0] == xfe and sig[1] == xff:
            encoding = 'utf-16-be'
            bom = sig[0:2]
        elif sig[0] == x00:
            encoding = 'utf-16-be'
        elif len(sig) >= 2 and sig[0] == xff and sig[1] == xfe:
            encoding = 'utf-16-le'
            bom = sig[0:2]
        elif len(sig) >= 2 and sig[1] == x00:
            encoding = 'utf-16-le'
        elif len(sig) >= 3 and sig[0] == xef and sig[1] == xbb and sig[2] == xbf:
            encoding = 'utf-8'
            bom = sig[0:3]
        else:
            encoding = 'utf-8'
    else:
        encoding = input_encoding

    return bom, encoding
