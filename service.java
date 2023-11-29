package com.example.service;

import com.example.dataaccess.notes.NotesDao;
import com.example.dataaccess.notes.NotesMemoryDao;
import com.example.dataaccess.notes.NotesMySQLDao;
import com.example.domain.Note;

import java.util.ArrayList;
import java.util.List;
import java.util.stream.Collectors;

public class TaskManagementService implements TaskManagement {
    private NotesDao notesDao = new NotesMySQLDao();
    // private NotesDao notesDao = new NotesMemoryDao();

    public boolean addNotes(Note note) {
        return this.notesDao.create(note);
    }

    public boolean removeNotes(String currentValue) {
        Note currentNote = new Note();
        currentNote.setNote(currentValue);
        return this.notesDao.delete(currentNote);
    }

    public boolean updateNotes(String currentValue, Note newNote) {
        Note currentNote = new Note();
        currentNote.setNote(currentValue);
        return this.notesDao.update(currentNote, newNote);
    }

    public List listAll() {
        return this.notesDao.read();
    }
}