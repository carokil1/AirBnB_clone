with patch('sys.stdout', new=StringIO()) as f:
    HBNBCommand().onecmd("help show")
