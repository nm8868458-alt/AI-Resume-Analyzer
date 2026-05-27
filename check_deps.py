try:
    import flask
    print("Flask ok")
    import pypdf
    print("pypdf ok")
    import docx
    print("python-docx ok")
    import google.generativeai
    print("google-generativeai ok")
except Exception as e:
    print(f"Missing: {e}")
