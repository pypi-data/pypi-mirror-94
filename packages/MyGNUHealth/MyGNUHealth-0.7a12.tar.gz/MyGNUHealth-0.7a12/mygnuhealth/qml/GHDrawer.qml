/**
 * SPDX-FileCopyrightText: 2020 Carl Schwan <schwancarl@kde.org>
 * 
 * SPDX-License-Identifier: GPL-2.0-or-later
 */

import org.kde.kirigami 2.10 as Kirigami

Kirigami.GlobalDrawer {
    required property bool isLoggedIn

    signal logout()

    isMenu: true

    actions: [
        Kirigami.Action {
            text: qsTr("Profile Settings")
            icon.name: "im-user"
            onTriggered: pageStack.layers.push(Qt.resolvedUrl("PageProfileSettings.qml"))
            enabled: isLoggedIn && pageStack.layers.depth === 1
        },
        Kirigami.Action {
            text: qsTr("Network Settings")
            icon.name: "network-connect"
            onTriggered: pageStack.layers.push(Qt.resolvedUrl("PageNetworkSettings.qml"))
            enabled: isLoggedIn && pageStack.layers.depth === 1
        },
        Kirigami.Action {
            text: qsTr("Logout")
            icon.name: "system-log-out"
            onTriggered: {
                // Clear the stack and go to the initial page
                pageStack.clear()
                pageStack.push(Qt.resolvedUrl("PageInitial.qml"))
            }
            enabled: isLoggedIn && pageStack.layers.depth === 1
        }
    ]
}
