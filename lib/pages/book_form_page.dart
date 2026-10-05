import 'package:flutter/material.dart';
import '../models/book.dart';

class BookFormPage extends StatefulWidget {
  const BookFormPage({super.key, this.book, required this.newId});
  final Book? book;
  final int newId;
  @override
  State<BookFormPage> createState() => _BookFormPageState();
}

class _BookFormPageState extends State<BookFormPage> {
  final _formKey = GlobalKey<FormState>();
  late final TextEditingController _title;
  late final TextEditingController _author;
  late final TextEditingController _notes;
  late ReadingStatus _status;

  @override
  void initState() {
    super.initState();
    _title = TextEditingController(text: widget.book?.title ?? '');
    _author = TextEditingController(text: widget.book?.author ?? '');
    _notes = TextEditingController(text: widget.book?.notes ?? '');
    _status = widget.book?.status ?? ReadingStatus.planned;
  }

  @override
  void dispose() {
    _title.dispose();
    _author.dispose();
    _notes.dispose();
    super.dispose();
  }

  void _save() {
    if (!_formKey.currentState!.validate()) return;
    Navigator.pop(
      context,
      Book(
        id: widget.book?.id ?? widget.newId,
        title: _title.text.trim(),
        author: _author.text.trim(),
        status: _status,
        notes: _notes.text.trim(),
      ),
    );
  }

  @override
  Widget build(BuildContext context) => Scaffold(
    appBar: AppBar(
      title: Text(widget.book == null ? 'Novo livro' : 'Editar livro'),
    ),
    body: SafeArea(
      child: Center(
        child: ConstrainedBox(
          constraints: const BoxConstraints(maxWidth: 640),
          child: SingleChildScrollView(
            padding: const EdgeInsets.all(24),
            child: Form(
              key: _formKey,
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.stretch,
                children: [
                  TextFormField(
                    key: const Key('titleField'),
                    controller: _title,
                    textCapitalization: TextCapitalization.sentences,
                    textInputAction: TextInputAction.next,
                    maxLength: 100,
                    decoration: const InputDecoration(labelText: 'Título'),
                    validator: (v) =>
                        (v ?? '').trim().isEmpty ? 'Informe o título' : null,
                  ),
                  const SizedBox(height: 16),
                  TextFormField(
                    key: const Key('authorField'),
                    controller: _author,
                    textCapitalization: TextCapitalization.words,
                    textInputAction: TextInputAction.next,
                    maxLength: 80,
                    decoration: const InputDecoration(
                      labelText: 'Autor ou autora',
                    ),
                    validator: (v) =>
                        (v ?? '').trim().isEmpty ? 'Informe a autoria' : null,
                  ),
                  const SizedBox(height: 16),
                  DropdownButtonFormField<ReadingStatus>(
                    key: const Key('statusField'),
                    initialValue: _status,
                    isExpanded: true,
                    decoration: const InputDecoration(
                      labelText: 'Situação de leitura',
                    ),
                    items: ReadingStatus.values
                        .map(
                          (s) =>
                              DropdownMenuItem(value: s, child: Text(s.label)),
                        )
                        .toList(),
                    onChanged: (s) => setState(() => _status = s!),
                  ),
                  const SizedBox(height: 24),
                  TextFormField(
                    key: const Key('notesField'),
                    controller: _notes,
                    maxLines: 3,
                    maxLength: 500,
                    decoration: const InputDecoration(
                      labelText: 'Notas (opcional)',
                    ),
                  ),
                  const SizedBox(height: 16),
                  FilledButton.icon(
                    key: const Key('saveButton'),
                    onPressed: _save,
                    icon: const Icon(Icons.check),
                    label: const Text('Salvar livro'),
                  ),
                  const SizedBox(height: 8),
                  TextButton(
                    onPressed: () => Navigator.pop(context),
                    child: const Text('Cancelar'),
                  ),
                ],
              ),
            ),
          ),
        ),
      ),
    ),
  );
}
