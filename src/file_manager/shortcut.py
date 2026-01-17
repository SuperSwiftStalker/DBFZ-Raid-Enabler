"""Windows shortcut (.lnk) creation and management."""

import win32com.client
from pathlib import Path
from typing import Optional
from utils.errors import ShortcutError
from utils.logger import logger


class ShortcutManager:
    """
    Create and manage Windows .lnk shortcuts.
    Uses win32com to create proper Windows shortcuts.
    """

    def create_shortcut(
        self,
        target_exe: Path,
        shortcut_path: Path,
        raid_name: str
    ) -> Path:
        """
        Create Windows shortcut with raid name in description.

        Args:
            target_exe: Path to executable the shortcut points to
            shortcut_path: Path where shortcut should be created (.lnk)
            raid_name: Raid boss name for description

        Returns:
            Path to the created shortcut

        Raises:
            ShortcutError: If shortcut creation fails
        """
        try:
            logger.info(f"Creating shortcut: {shortcut_path}")

            # Create shell object
            shell = win32com.client.Dispatch("WScript.Shell")

            # Create shortcut object
            shortcut = shell.CreateShortCut(str(shortcut_path))

            # Set properties
            shortcut.TargetPath = str(target_exe)
            shortcut.WorkingDirectory = str(target_exe.parent)
            shortcut.Description = f"DBFZ Raid: {raid_name}"
            shortcut.IconLocation = str(target_exe)  # Use exe icon

            # Save shortcut
            shortcut.save()

            logger.info(f"Shortcut created successfully: {raid_name}")
            return shortcut_path

        except Exception as e:
            logger.error(f"Failed to create shortcut: {e}")
            raise ShortcutError(f"Failed to create shortcut: {e}")

    def update_shortcut(
        self,
        target_exe: Path,
        shortcut_path: Path,
        raid_name: str
    ) -> Path:
        """
        Update existing shortcut with new raid name.

        Simply deletes old shortcut and creates new one.
        This is simpler than trying to modify the existing shortcut.

        Args:
            target_exe: Path to executable
            shortcut_path: Path to shortcut file
            raid_name: New raid boss name

        Returns:
            Path to the created (updated) shortcut

        Raises:
            ShortcutError: If update fails
        """
        # Delete old shortcut if it exists
        if shortcut_path.exists():
            try:
                logger.info(f"Removing old shortcut: {shortcut_path}")
                shortcut_path.unlink()
            except Exception as e:
                logger.warning(f"Could not remove old shortcut: {e}")
                # Continue anyway - will overwrite

        # Create new shortcut
        return self.create_shortcut(target_exe, shortcut_path, raid_name)

    def get_shortcut_target(self, shortcut_path: Path) -> Optional[str]:
        """
        Read target path from existing shortcut.

        Args:
            shortcut_path: Path to shortcut file

        Returns:
            Target path as string, or None if cannot read
        """
        if not shortcut_path.exists():
            logger.debug(f"Shortcut doesn't exist: {shortcut_path}")
            return None

        try:
            shell = win32com.client.Dispatch("WScript.Shell")
            shortcut = shell.CreateShortCut(str(shortcut_path))
            target = shortcut.TargetPath

            logger.debug(f"Shortcut target: {target}")
            return target

        except Exception as e:
            logger.error(f"Failed to read shortcut: {e}")
            return None

    def shortcut_exists(self, shortcut_path: Path) -> bool:
        """
        Check if shortcut exists and is valid.

        Args:
            shortcut_path: Path to check

        Returns:
            True if shortcut exists and appears valid
        """
        if not shortcut_path.exists():
            return False

        # Try to read target to verify it's a valid shortcut
        target = self.get_shortcut_target(shortcut_path)
        return target is not None
