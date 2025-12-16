# Daily Diet API - Design de Sistema

Este documento descreve a arquitetura, as regras de negócio e os endpoints da API de controle de dieta diária.

## 1. Estrutura de Dados (Modelos)

O sistema utiliza um banco de dados relacional com duas entidades principais conectadas por um relacionamento de um-para-muitos (1:N).

### Entidade: Usuário (User)
Responsável por armazenar as credenciais e o nível de acesso ao sistema.
- **id**: Identificador único (UUID) para garantir a segurança dos dados.
- **username**: Nome de usuário único para autenticação.
- **password**: Senha armazenada via hash criptográfico (nunca texto plano).
- **role**: Define as permissões do sistema (`user` ou `admin`).

### Entidade: Refeição (Meal)
Registros individuais de alimentação.
- **id**: Identificador único da refeição.
- **name**: Nome curto (ex: "Almoço de Domingo").
- **description**: Detalhamento do que foi consumido.
- **date_time**: Data e hora do registro (Formato ISO 8601).
- **is_on_diet**: Booleano indicando se a refeição está dentro do plano alimentar.
- **user_id**: Chave estrangeira ligada ao ID do Usuário.

---

## 2. Matriz de Papéis e Permissões

### Papel: Administrador (Admin)
O Administrador atua como supervisor e não registra dietas próprias.
- **Visualização**: Pode listar todos os usuários e ver as refeições de qualquer um.
- **Edição/Exclusão Geral**: Pode atualizar ou deletar qualquer usuário ou refeição.
- **Regra de Segurança**: Não pode deletar a própria conta (exige outro admin para tal).
- **Restrição**: Não possui permissão para criar refeições para si mesmo.

### Papel: Usuário Comum (User)
O Usuário é focado no controle pessoal de sua saúde.
- **Gestão Pessoal**: Pode criar, visualizar, editar e deletar suas próprias refeições.
- **Autodeleção**: Pode excluir sua própria conta após estar devidamente logado.
- **Restrição**: Não possui acesso a dados de outros usuários ou à listagem global de perfis.

---

## 3. Endpoints da API

### Autenticação
| Método | Rota | Descrição | Acesso |
| :--- | :--- | :--- | :--- |
| `POST` | `/register` | Registra um novo usuário (padrão 'user') | Público |
| `POST` | `/login` | Autentica o usuário e inicia a sessão | Público |
| `POST` | `/logout` | Encerra a sessão ativa | Autenticado |

### Perfil e Dieta do Usuário
| Método | Rota | Descrição | Acesso |
| :--- | :--- | :--- | :--- |
| `GET` | `/me` | Vê meus dados de perfil | User |
| `PUT` | `/me` | Atualiza senha do usuário | User |
| `DELETE` | `/me` | Deleção da própria conta | User |
| `POST` | `/me/meals` | Registra uma nova refeição | User |
| `GET` | `/me/meals` | Lista todas as refeições | User |
| `GET` | `/me/meals/<id>` | Vê detalhes de uma refeição | User |
| `PUT` | `/me/meals/<id>` | Edita uma refeição | User |
| `DELETE` | `/me/meals/<id>` | Apaga uma refeição | User |

### Painel Administrativo
| Método | Rota | Descrição | Acesso |
| :--- | :--- | :--- | :--- |
| `GET` | `/admin/users` | Lista todos os usuários do sistema | Admin |
| `GET` | `/admin/users/<user_id>` | Vê perfil completo de um usuário específico | Admin |
| `PUT` | `/admin/users/<user_id>` | Atualiza dados de um usuário específico | Admin |
| `DELETE` | `/admin/users/<user_id>` | Deleta um usuário específico (bloqueado se for o próprio admin logado) | Admin |
| `GET` | `/admin/users/<user_id>/meals` | Vê todas as refeições de um usuário específico | Admin |
| `GET` | `/admin/users/<user_id>/meals/<meal_id>` | Vê detalhes de uma refeição de um usuário | Admin |
| `PUT` | `/admin/users/<user_id>/meals/<meal_id>` | Atualiza dados de uma refeição de um usuário | Admin |
| `DELETE` | `/admin/users/<user_id>/meals/<meal_id>` | Deleta uma refeição de um usuário | Admin |