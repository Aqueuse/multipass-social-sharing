def subtask_exist(connection, social_network, task_id):
    cursor = connection.cursor()

    social_network_table = social_network+"Task"
    cursor.execute("SELECT * FROM ? WHERE task_id=?", (social_network_table, task_id))
    social_network_task = cursor.fetchall()

    if len(social_network_task) == 0:
        return false
    return true
