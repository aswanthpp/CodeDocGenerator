package com.example.dataaccess.notes;

import com.example.dataaccess.mysql.DatabaseManager;
import com.example.domain.Note;

import java.sql.*;
import java.util.ArrayList;
import java.util.List;

public class NotesMySQLDao implements NotesDao {
    public boolean create(Note note) {
        Connection connection = null;
        try {
            connection = DatabaseManager.getConnection();
            connection.setAutoCommit(false);  //
            PreparedStatement statement = null;
            String insertNote = "Insert into my_notes(note) values(?)";
            statement = connection.prepareStatement(insertNote);
            statement.setString(1, note.getNote());
            if (statement.executeUpdate() == 1) {
                connection.commit();
                connection.close();
                return true;
            } else {
                connection.close();
                return false;
            }
        } catch (SQLException e) {
            e.printStackTrace();
            return false;
        }
}

    public List read() {
        Connection connection = null;
        PreparedStatement preparedStatement = null;
        ResultSet resultSet = null;
        List<Note> notes = new ArrayList<Note>();
        try {
            String listAll = "SELECT note FROM my_notes";
            connection = DatabaseManager.getConnection();
            preparedStatement = connection.prepareStatement(listAll);
            resultSet = preparedStatement.executeQuery();
            while (resultSet.next()) {
                Note note = new Note();
                note.setNote(resultSet.getString("note"));
                notes.add(note);
            }
            connection.close();
        } catch (SQLException throwables) {
            throwables.printStackTrace();
        }

        return notes;
    }

    public boolean update(Note currentNote,Note newNote) {
        Connection connection=null;
        PreparedStatement preparedStatement = null;
        try{
            connection=DatabaseManager.getConnection();
            connection.setAutoCommit(false);
            String updateString="UPDATE my_notes SET note = ? where note=?";
            preparedStatement = connection.prepareStatement(updateString);
            preparedStatement.setString(2,currentNote.getNote());
            preparedStatement.setString(1,newNote.getNote());

            if(preparedStatement.executeUpdate()==1){
                connection.commit();
                connection.close();
                return true;
            }else{
                connection.close();
                return false;
            }

        } catch (SQLException throwables) {
            throwables.printStackTrace();
            return false;
        }

    }

    public boolean delete(Note currentNote) {
        Connection connection=null;
        PreparedStatement preparedStatement=null;
        try{
            String deleteQuery="delete from my_notes where note=?";
            connection=DatabaseManager.getConnection();
            preparedStatement=connection.prepareStatement(deleteQuery);
            preparedStatement.setString(1,currentNote.getNote());
            if(preparedStatement.executeUpdate()==1){
                connection.close();
                return true;
            }else{
                connection.close();
                return false;
            }
        } catch (SQLException throwables) {
            throwables.printStackTrace();
            return false;
        }
    }
}
