import 'package:flutter/material.dart';
import '../models/book.dart';
import 'book_form_page.dart';

class BookDetailPage extends StatelessWidget {
  const BookDetailPage({super.key, required this.book});
  final Book book;

  Future<void> _edit(BuildContext context) async {
    final updated = await Navigator.push<Book>(
      context,
      MaterialPageRoute(
        builder: (_) => BookFormPage(book: book, newId: book.id),
      ),
    );
    if (context.mounted && updated != null) Navigator.pop(context, updated);
  }

  @override
  Widget build(BuildContext context) => Scaffold(
    appBar: AppBar(title: const Text('Detalhes do livro')),
    body: SafeArea(
      child: Align(
        alignment: Alignment.topCenter,
        child: ConstrainedBox(
          constraints: const BoxConstraints(maxWidth: 640),
          child: SingleChildScrollView(
            padding: const EdgeInsets.all(24),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.stretch,
              children: [
                const Icon(Icons.menu_book_outlined, size: 72),
                const SizedBox(height: 24),
                Text(
                  book.title,
                  style: Theme.of(context).textTheme.headlineMedium,
                ),
                const SizedBox(height: 12),
                Text(
                  'Autoria: ${book.author}',
                  style: Theme.of(context).textTheme.titleMedium,
                ),
                const SizedBox(height: 20),
                Text('Situação: ${book.status.label}'),
                const Divider(height: 40),
                Text('Notas', style: Theme.of(context).textTheme.titleMedium),
                const SizedBox(height: 8),
                Text(
                  book.notes.isEmpty ? 'Sem notas adicionadas.' : book.notes,
                ),
                const SizedBox(height: 32),
                FilledButton.icon(
                  onPressed: () => _edit(context),
                  icon: const Icon(Icons.edit_outlined),
                  label: const Text('Editar livro'),
                ),
              ],
            ),
          ),
        ),
      ),
    ),
  );
}
