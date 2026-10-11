const vscode = require('vscode');
const path = require('path');

function activate(context) {
    let disposable1 = vscode.commands.registerCommand('sourcerer.generateSours', (uri) => {
        if (validateUri(uri)) return

        const workspaceFolder = vscode.workspace.workspaceFolders?.[0]?.uri.fsPath;
        workPythonCode(`createSours --file "${uri.fsPath}"`, workspaceFolder)

        vscode.window.showInformationMessage(`Генерация запущена для: ${path.basename(targetFile)}`);
    });
    context.subscriptions.push(disposable1);

    let disposable2 = vscode.commands.registerCommand('sourcerer.generateTab', (uri) => {
        if (validateUri(uri)) return

        const workspaceFolder = vscode.workspace.workspaceFolders?.[0]?.uri.fsPath;
        workPythonCode(`createClass --file "${uri.fsPath}"`, workspaceFolder)

        vscode.window.showInformationMessage(`Генерация запущена для: ${path.basename(targetFile)}`);
    });
    context.subscriptions.push(disposable2);
}

function validateUri(uri) {
    if (!uri) return true;

    const workspaceFolder = vscode.workspace.workspaceFolders?.[0]?.uri.fsPath;
    if (!workspaceFolder) {
        vscode.window.showErrorMessage('Ошибка: Не найдена корневая папка проекта!');
        return true;
    }

    return false
}

function workPythonCode(commandPy, workspaceFolder) {
    // Формируем команду как в твоем launch.json
    const mainPy = path.join(workspaceFolder, 'main.py');

    // 1. Получаем путь к выбранному интерпретатору
    const pythonPath = vscode.workspace.getConfiguration('python').get('defaultInterpreterPath')
        || 'python'; // Фолбэк, если настройка не задана

    // 2. Формируем команду с правильным питоном
    const command = `& "${pythonPath}" "${mainPy}" ${commandPy}`;

    // Создаем терминал и запускаем
    const terminal = vscode.window.createTerminal({
        name: 'Sourcerer Gen',
        cwd: workspaceFolder
    });

    terminal.show();
    terminal.sendText(command);
}

exports.activate = activate;