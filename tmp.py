        curr.execute("SELECT EXISTS(SELECT 1 FROM FORMIMP)")
        is_empty = not cur.fetchone()[0]
        if is_empty:
            curr.execute("""
                    INSERT INTO formimp (
                    id, s_code, s_descrip, s_valparam, d_creat, d_modif, s_usercreat,
                    s_usermodif
                    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s);
                    """, (1, "DOSFORM", "inputs files path", "C:/testform", datetime.now().strftime("%Y-%m-%d %H:%M:%S"), datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "user", "user"))