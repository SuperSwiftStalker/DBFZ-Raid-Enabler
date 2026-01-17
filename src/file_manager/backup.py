"""Backup management for clean game executable."""

import shutil
from pathlib import Path
from typing import Optional
from utils.errors import BackupError
from utils.logger import logger


class BackupManager:
    """
    Manage clean backup and patched executable lifecycle.
    """

    def verify_clean_exe(self, clean_exe: Path) -> bool:
        """
        Verify that clean exe exists.

        Args:
            clean_exe: Path to original game executable

        Returns:
            True if clean exe exists

        Raises:
            BackupError: If clean exe doesn't exist
        """
        if not clean_exe.exists():
            logger.error(f"Clean executable not found: {clean_exe}")
            raise BackupError(
                f"Original game executable not found at {clean_exe}. "
                "Please verify game files via Steam."
            )

        logger.info(f"Clean exe verified: {clean_exe}")
        return True

    def create_or_update_patched_exe(
        self,
        clean_exe: Path,
        patched_exe: Path
    ) -> Path:
        """
        Create/update patched exe from clean exe.

        This workflow ensures we always patch from a clean source:
        1. Verify clean exe exists
        2. Delete old patched exe if it exists
        3. Copy clean exe to patched exe location
        4. Return path to patched exe for patching

        Args:
            clean_exe: Path to original executable (never modified)
            patched_exe: Path to patched executable (will be created/overwritten)

        Returns:
            Path to patched exe (ready for patching)

        Raises:
            BackupError: If any operation fails
        """
        # Verify clean exe exists
        self.verify_clean_exe(clean_exe)

        # Remove old patched exe if it exists
        if patched_exe.exists():
            try:
                logger.info(f"Removing old patched exe: {patched_exe}")
                patched_exe.unlink()
            except Exception as e:
                logger.warning(f"Could not remove old patched exe: {e}")
                # Continue anyway - copy will overwrite

        # Copy clean exe to patched exe location
        try:
            logger.info(f"Creating fresh patched exe from clean exe")
            shutil.copy2(clean_exe, patched_exe)
            logger.info(f"Patched exe ready: {patched_exe}")
            return patched_exe
        except Exception as e:
            logger.error(f"Failed to create patched exe: {e}")
            raise BackupError(f"Failed to create patched exe: {e}")

    def detect_current_patch(self, patched_exe: Path) -> Optional[int]:
        """
        Detect which raid is currently patched (if any).

        Scans the patched exe for the raid index in the known patch pattern.
        Looks for: B8 [4 bytes] 90 (mov eax, immediate; nop)

        Args:
            patched_exe: Path to patched executable

        Returns:
            Raid index (1-38) or None if not patched or cannot detect
        """
        if not patched_exe.exists():
            logger.debug("Patched exe doesn't exist")
            return None

        try:
            exe_data = patched_exe.read_bytes()

            # Look for pattern: B8 [4 bytes] 90
            pattern_start = 0xB8
            pattern_end = 0x90

            for i in range(len(exe_data) - 5):
                if exe_data[i] == pattern_start and exe_data[i + 5] == pattern_end:
                    # Extract 4-byte raid index (little-endian)
                    raid_bytes = exe_data[i + 1:i + 5]
                    raid_index = int.from_bytes(raid_bytes, byteorder='little')

                    # Validate raid index (1-38)
                    if 1 <= raid_index <= 38:
                        logger.info(f"Detected current patch: Raid {raid_index}")
                        return raid_index

            logger.debug("No valid raid patch detected")
            return None

        except Exception as e:
            logger.error(f"Failed to detect current patch: {e}")
            return None

    def cleanup_all(self, patched_exe: Path, game_root: Path) -> dict:
        """
        Clean up all modifications made by the program.

        Removes:
        - Patched executable
        - All raid shortcuts (in game folder)

        Note: Clean exe is never modified, so nothing to restore.

        Args:
            patched_exe: Path to patched executable
            game_root: Path to game root directory

        Returns:
            Dictionary with cleanup results:
            {
                'patched_exe_removed': bool,
                'shortcuts_removed': int,
                'errors': [str]
            }
        """
        import os

        results = {
            'patched_exe_removed': False,
            'shortcuts_removed': 0,
            'errors': []
        }

        # Remove patched exe
        if patched_exe.exists():
            try:
                logger.info(f"Removing patched exe: {patched_exe}")
                patched_exe.unlink()
                results['patched_exe_removed'] = True
                logger.info("Patched exe removed successfully")
            except Exception as e:
                error_msg = f"Failed to remove patched exe: {e}"
                logger.error(error_msg)
                results['errors'].append(error_msg)
        else:
            logger.info("Patched exe not found, nothing to remove")

        # Remove all shortcuts in game root folder
        try:
            for shortcut in game_root.glob("DBFZ Raid *.lnk"):
                try:
                    logger.info(f"Removing shortcut: {shortcut.name}")
                    shortcut.unlink()
                    results['shortcuts_removed'] += 1
                except Exception as e:
                    error_msg = f"Failed to remove shortcut {shortcut.name}: {e}"
                    logger.error(error_msg)
                    results['errors'].append(error_msg)
        except Exception as e:
            error_msg = f"Error scanning for shortcuts in game folder: {e}"
            logger.error(error_msg)
            results['errors'].append(error_msg)

        return results
