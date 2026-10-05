import 'package:flutter/material.dart';

class EmptyCatalog extends StatelessWidget {
  const EmptyCatalog({super.key, required this.onAdd});
  final VoidCallback onAdd;

  @override
  Widget build(BuildContext context) => Center(
    child: SingleChildScrollView(
      padding: const EdgeInsets.all(24),
      child: Column(
        mainAxisSize: MainAxisSize.min,
        children: [
          const Icon(Icons.menu_book_outlined, size: 64),
          const SizedBox(height: 20),
          Text(
            'Nenhum livro cadastrado',
            textAlign: TextAlign.center,
            style: Theme.of(context).textTheme.headlineSmall,
          ),
          const SizedBox(height: 8),
          const Text(
            'Guarde aqui suas leituras e próximos livros.',
            textAlign: TextAlign.center,
          ),
          const SizedBox(height: 24),
          FilledButton.icon(
            onPressed: onAdd,
            icon: const Icon(Icons.add),
            label: const Text('Adicionar primeiro livro'),
          ),
        ],
      ),
    ),
  );
}
