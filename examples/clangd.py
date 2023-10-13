import pylspclient
import subprocess
import threading
import argparse
import linecache
import urllib.parse


def extractFilePath(uri):
    file_path = urllib.parse.unquote(uri)

    idx = uri.find("file://")
    if idx > -1:
        file_path = file_path[idx+7:]

    return file_path


def showInterpretation(loc):
    file_path = extractFilePath(loc.uri)
    code_line = loc.range.start.line+1
    linestr = linecache.getline(file_path, code_line)

    idx_start = loc.range.start.character
    idx_end = loc.range.end.character

    print("INTERP:")
    print("  File: " + file_path)
    print("  Loc:  " + str(code_line) + ":" +
          str(idx_start+1) + ":" + str(idx_end))
    print("  Data: |" + linestr[idx_start:idx_end] + "|")


def showInterpretations(locations):
    for loc in locations:
        showInterpretation(loc)


def interpTextDocumentDefinition(locations):
    showInterpretations(locations)


def interpTextDocumentTypeReferences(references):
    showInterpretations(references)


class ReadPipe(threading.Thread):
    def __init__(self, pipe):
        threading.Thread.__init__(self)
        self.pipe = pipe

    def run(self):
        line = self.pipe.readline().decode("utf-8")
        while line:
            print(line)
            line = self.pipe.readline().decode("utf-8")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="pylspclient example with clangd")
    parser.add_argument(
        "clangd_path",
        type=str,
        default="/home/vistdn/.local/share/nvim/mason/bin/clangd",
        help="the clangd path",
        nargs="?",
    )
    args = parser.parse_args()
    p = subprocess.Popen(
        [args.clangd_path],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    read_pipe = ReadPipe(p.stderr)
    read_pipe.start()
    json_rpc_endpoint = pylspclient.JsonRpcEndpoint(p.stdin, p.stdout)
    # To work with socket: sock_fd = sock.makefile()
    lsp_endpoint = pylspclient.LspEndpoint(json_rpc_endpoint)

    lsp_client = pylspclient.LspClient(lsp_endpoint)
    capabilities = {
        "textDocument": {
            "codeAction": {"dynamicRegistration": True},
            "codeLens": {"dynamicRegistration": True},
            "colorProvider": {"dynamicRegistration": True},
            "completion": {
                "completionItem": {
                    "commitCharactersSupport": True,
                    "documentationFormat": ["markdown", "plaintext"],
                    "snippetSupport": True,
                },
                "completionItemKind": {
                    "valueSet": [
                        1,
                        2,
                        3,
                        4,
                        5,
                        6,
                        7,
                        8,
                        9,
                        10,
                        11,
                        12,
                        13,
                        14,
                        15,
                        16,
                        17,
                        18,
                        19,
                        20,
                        21,
                        22,
                        23,
                        24,
                        25,
                    ]
                },
                "contextSupport": True,
                "dynamicRegistration": True,
            },
            "definition": {"dynamicRegistration": True},
            "documentHighlight": {"dynamicRegistration": True},
            "documentLink": {"dynamicRegistration": True},
            "documentSymbol": {
                "dynamicRegistration": True,
                "symbolKind": {
                    "valueSet": [
                        1,
                        2,
                        3,
                        4,
                        5,
                        6,
                        7,
                        8,
                        9,
                        10,
                        11,
                        12,
                        13,
                        14,
                        15,
                        16,
                        17,
                        18,
                        19,
                        20,
                        21,
                        22,
                        23,
                        24,
                        25,
                        26,
                    ]
                },
            },
            "formatting": {"dynamicRegistration": True},
            "hover": {
                "contentFormat": ["markdown", "plaintext"],
                "dynamicRegistration": True,
            },
            "implementation": {"dynamicRegistration": True},
            "onTypeFormatting": {"dynamicRegistration": True},
            "publishDiagnostics": {"relatedInformation": True},
            "rangeFormatting": {"dynamicRegistration": True},
            "references": {"dynamicRegistration": True},
            "rename": {"dynamicRegistration": True},
            "signatureHelp": {
                "dynamicRegistration": True,
                "signatureInformation": {
                    "documentationFormat": ["markdown", "plaintext"]
                },
            },
            "synchronization": {
                "didSave": True,
                "dynamicRegistration": True,
                "willSave": True,
                "willSaveWaitUntil": True,
            },
            "typeDefinition": {"dynamicRegistration": True},
        },
        "workspace": {
            "applyEdit": True,
            "configuration": True,
            "didChangeConfiguration": {"dynamicRegistration": True},
            "didChangeWatchedFiles": {"dynamicRegistration": True},
            "executeCommand": {"dynamicRegistration": True},
            "symbol": {
                "dynamicRegistration": True,
                "symbolKind": {
                    "valueSet": [
                        1,
                        2,
                        3,
                        4,
                        5,
                        6,
                        7,
                        8,
                        9,
                        10,
                        11,
                        12,
                        13,
                        14,
                        15,
                        16,
                        17,
                        18,
                        19,
                        20,
                        21,
                        22,
                        23,
                        24,
                        25,
                        26,
                    ]
                },
            },
            "workspaceEdit": {"documentChanges": True},
            "workspaceFolders": True,
        },
    }
    root_path = "/home/vistdn/Misc/Tests/05_python/000_libclang_cindex/example/"
    root_uri = "file://" + root_path
    workspace_folders = [{"name": "python-lsp", "uri": root_uri}]
    print(
        lsp_client.initialize(
            p.pid, None, root_uri, None, capabilities, "off", workspace_folders
        )
    )
    print(lsp_client.initialized())

    # file_path = "/home/vistdn/Misc/Tests/05_python/000_libclang_cindex/example/my_app/src/main.cpp"
    file_path = "/home/vistdn/Workspace/Repos/microsar-adaptive-worktrees/r7-UMAMI-1/BSW/amsr-vector-fs-per-libpersistency/lib/persistency-key-value-storage/include/ara/per/key_value_storage.h"
    uri = "file://" + file_path
    text = open(file_path, "r").read()
    languageId = pylspclient.lsp_structs.LANGUAGE_IDENTIFIER.C
    version = 1
    lsp_client.didOpen(
        pylspclient.lsp_structs.TextDocumentItem(
            uri, languageId, version, text))

    print("\n====== Tests ==================================")

    # try:
    #     symbols = lsp_client.documentSymbol(
    #         pylspclient.lsp_structs.TextDocumentIdentifier(uri)
    #     )
    #     for symbol in symbols:
    #         print(symbol.name)
    # except pylspclient.lsp_structs.ResponseError:
    #     # documentSymbol is supported from version 8.
    #     print("Failed to document symbols")

    # print("\n\n  --- textDocument/documentSymbol ---\n")
    # response = lsp_client.documentSymbol(
    #     pylspclient.lsp_structs.TextDocumentIdentifier(uri))
    # interpTextDocumentDocumentSymbol(response)
    #
    # print("\n\n  --- textDocument/declaration ---\n")
    # response = lsp_client.declaration(
    #     pylspclient.lsp_structs.TextDocumentIdentifier(uri),
    #     pylspclient.lsp_structs.Position(161, 16))
    # interpTextDocumentDeclaration(response)
    #
    # print("\n  --- textDocument/definition ---\n")
    # response = lsp_client.definition(
    #     pylspclient.lsp_structs.TextDocumentIdentifier(uri),
    #     pylspclient.lsp_structs.Position(161, 16))
    # interpTextDocumentDefinition(response)
    #
    # print("\n  --- textDocument/typeDefinition ---\n")
    # response = lsp_client.typeDefinition(
    #     pylspclient.lsp_structs.TextDocumentIdentifier(uri),
    #     pylspclient.lsp_structs.Position(161, 16))
    # interpTextDocumentTypeDefinition(response)
    #
    # print("\n\n  --- textDocument/signatureHelp ---\n")
    # response = lsp_client.signatureHelp(
    #     pylspclient.lsp_structs.TextDocumentIdentifier(uri),
    #     pylspclient.lsp_structs.Position(129, 25))
    # interpTextDocumentTypeSignatureHelp(response)
    #
    # print("\n\n  --- textDocument/references ---\n")
    # response = lsp_client.definition(
    #     pylspclient.lsp_structs.TextDocumentIdentifier(uri),
    #     pylspclient.lsp_structs.Position(129, 25))
    # interpTextDocumentTypeDefinition(response)
    # response = lsp_client.references(
    #     pylspclient.lsp_structs.TextDocumentIdentifier(uri),
    #     pylspclient.lsp_structs.Position(129, 25))
    # interpTextDocumentTypeReferences(response)

    # lsp_client.completion(
    #     pylspclient.lsp_structs.TextDocumentIdentifier(uri),
    #     pylspclient.lsp_structs.Position(14, 4),
    #     pylspclient.lsp_structs.CompletionContext(
    #         pylspclient.lsp_structs.CompletionTriggerKind.Invoked
    #     ),
    # )

    # print("\n  --- textDocument/definition ---\n")
    # response = lsp_client.definition(
    #     pylspclient.lsp_structs.TextDocumentIdentifier(uri),
    #     pylspclient.lsp_structs.Position(358, 21))
    # # pylspclient.lsp_structs.Position(354, 11))
    # # pylspclient.lsp_structs.Position(356, 10))
    # interpTextDocumentDefinition(response)

    # TODO: Implement Hover
    # print("\n  --- textDocument/hover ---\n")

    # TODO: Implement FoldingRange
    # print("\n  --- textDocument/foldingRange ---\n")

    print("\n===============================================\n")

    lsp_client.shutdown()
    lsp_client.exit()
