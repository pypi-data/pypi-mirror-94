## @file module.py
#  @author Scott Miller
#  @version 1.0
#  @date November 17, 2016
#  @copyright Zymbit, Inc.
#  @brief Python interface class to Zymkey Application Utilities Library.
#  @details
#  This file contains a Python class which interfaces to the the Zymkey
#  Application Utilities library. This class facilitates writing user
#  space applications which use Zymkey to perform cryptographic
#  operations, such as:
#       1. Signing of payloads using ECDSA
#       2. Verification of payloads that were signed using Zymkey
#       3. Exporting the public key that matches Zymkey's private key
#       4. "Locking" and "unlocking" data objects
#       5. Generating random data
#  Additionally, there are methods for changing the i2c address (i2c units
#  only), setting tap sensitivity and controlling the LED.
from __future__ import absolute_import

import hashlib
import os
import errno

from ctypes import *

import distutils.sysconfig

from .exceptions import VerificationError, ZymkeyLibraryError, ZymkeyTimeoutError
from .settings import ZYMKEY_LIBRARY_PATH
from .utils import is_string

CLOUD_ENCRYPTION_KEY = 'cloud'
ZYMKEY_ENCRYPTION_KEY = 'zymkey'

ENCRYPTION_KEYS = (
   CLOUD_ENCRYPTION_KEY,
   ZYMKEY_ENCRYPTION_KEY
)

keyTypes = {
    "secp256r1" : 0,
    "nistp256"  : 0,
    "secp256k1" : 1
}

kdfFuncTypes = {
    "none"           : 0,
    "rfc5869-sha256" : 1,
    "rfc5869-sha512" : 2,
    "pbkdf2-sha256"  : 3,
    "pbkdf2-sha512"  : 4
}

zkalib = None
prefixes = []
for prefix in (distutils.sysconfig.get_python_lib(), ''):
   _zymkey_library_path = '{}{}'.format(prefix, ZYMKEY_LIBRARY_PATH)
   if os.path.exists(_zymkey_library_path):
      zkalib = cdll.LoadLibrary(_zymkey_library_path)
      break
   else:
      prefixes.append(os.path.dirname(_zymkey_library_path))
else:
    raise ZymkeyLibraryError('unable to find {}, checked {}'.format(os.path.basename(ZYMKEY_LIBRARY_PATH), prefixes))

## @brief Return class for Zymkey.get_accelerometer_data
#  @details This class is the return type for Zymkey.get_accelerometer_data. It
#           contains the instantaneous reading of an axis along with the
#           direction of force that caused the latest tap event.

## @brief The Zymkey class definition
#  @details
#  This class provides access to the Zymkey within Python
class Zymkey(object):
   EPHEMERAL_KEY_SLOT = -1

   ## @name Zymkey Context
   ###@{

   ## @brief The class initialization opens and stores an instance of a
   #  Zymkey context
   def __init__(self):
      self._zk_ctx = c_void_p()
      ret = self._zkOpen(byref(self._zk_ctx))
      if ret < 0:
         raise AssertionError("bad return code {!r}".format(ret))

   ## @brief The class destructor closes a Zymkey context
   def __del__(self):
      if self._zk_ctx != None:
         ret = self._zkClose(self._zk_ctx)
         if ret < 0:
            raise AssertionError('bad return code %d' % ret)
         self._zk_ctx = None
   ###@}

   ## @name LED Control
   ###@{

   ## @brief Turn the LED on
   def led_on(self):
      ret = self._zkLEDOn(self._zk_ctx)
      if ret < 0:
         raise AssertionError('bad return code %d' % ret)

   ## @brief Turn the LED off
   def led_off(self):
      ret = self._zkLEDOff(self._zk_ctx)
      if ret < 0:
         raise AssertionError('bad return code %d' % ret)

   ## @brief Flash the LED
   #  @param on_ms  The amount of time in milliseconds that the LED
   #    will be on for
   #  @param off_ms The amount of time in milliseconds that the LED
   #    will be off for. If this parameter is set to 0 (default), the
   #    off time is the same as the on time.
   #  @param num_flashes The number of on/off cycles to execute. If
   #    this parameter is set to 0 (default), the LED flashes
   #    indefinitely.
   def led_flash(self, on_ms, off_ms=0, num_flashes=0):
      if off_ms == 0:
         off_ms = on_ms
      ret = self._zkLEDFlash(self._zk_ctx, on_ms, off_ms, num_flashes)
      if ret < 0:
         raise AssertionError('bad return code %d' % ret)
   ###@}

   ## @name Random Number Generation
   ###@{

   ## @brief Get some random bytes
   #  @param num_bytes The number of random bytes to get
   def get_random(self, num_bytes):
      rdata = c_void_p()
      ret = self._zkGetRandBytes(self._zk_ctx, byref(rdata), num_bytes)
      if ret < 0:
         raise AssertionError('bad return code %d' % ret)
      rc = (c_ubyte * num_bytes).from_address(rdata.value)
      rd_array = bytearray(rc)
      return rd_array

   ## @brief Deposit random data in a file
   #  @param file_path    The absolute path name for the destination file
   #  @param num_bytes The number of random bytes to get
   def create_random_file(self, file_path, num_bytes):
      ret = self._zkCreateRandDataFile(self._zk_ctx, file_path.encode('utf-8'), num_bytes)
      if ret < 0:
         raise AssertionError('bad return code %d' % ret)
   ###@}

   ## @name Lock Data
   ###@{

   ## @brief Lock up source (plaintext) data
   #  @details This method encrypts and signs a block of data.
   #  @details
   #    The zymkey has two keys that can be used for locking/unlocking
   #    operations, designated as 'shared' and 'one-way'.
   #      1. The one-way key is meant to lock up data only on the
   #         local host computer. Data encrypted using this key cannot
   #         be exported and deciphered anywhere else.
   #      2. The shared key is meant for publishing data to other
   #         sources that have the capability to generate the shared
   #         key, such as the Zymbit cloud server.
   #
   #  @param src The source (plaintext) data. If typed as a basestring,
   #    it is assumed to be an absolute file name path where the source
   #    file is located, otherwise it is assumed to contain binary
   #    data.
   #  @param dst The destination (ciphertext) data. If specified as a
   #    basestring, it is assumed to be an absolute file name path
   #    where the destination data is meant to be deposited. Otherwise,
   #    the locked data result is returned from the method call as a
   #    bytearray. The default is 'None', which means that the data
   #    will be returned to the caller as a bytearray.
   #  @param encryption_key Specifies which key will be
   #    used to lock the data up. A value of 'zymkey' (default)
   #    specifies that the Zymkey will use the one-way key. A value of
   #   'cloud' specifies that the shared key is used. Specify 'cloud' for
   #    publishing data to some other source that is able to derive the
   #    shared key (e.g. Zymbit cloud) and 'zymkey' when the data is
   #    meant to reside exclusively within the host computer.
   def lock(self, src, dst=None, encryption_key=ZYMKEY_ENCRYPTION_KEY):
      # Determine if source and destination are strings. If so, they must be
      # filenames
      src_is_file = is_string(src)
      dst_is_file = is_string(dst)
      # Prepare src if it is not specifying a filename
      if not src_is_file:
         src_sz = len(src)
         src_c_ubyte = (c_ubyte * src_sz)(*src)
      else:
         src = src.encode('utf-8')
      # Prepare dst if it is not specifying a filename
      if not dst_is_file:
         dst_data = c_void_p()
         dst_data_sz = c_int()
      else:
         dst = dst.encode('utf-8')

      assert encryption_key in ENCRYPTION_KEYS
      use_shared_key = encryption_key == CLOUD_ENCRYPTION_KEY

      if src_is_file and dst_is_file:
         ret = self._zkLockDataF2F(self._zk_ctx,
                             src,
                             dst,
                             use_shared_key)
         if ret < 0:
            raise AssertionError('bad return code %d' % ret)

      if not src_is_file and dst_is_file:
         ret = self._zkLockDataB2F(self._zk_ctx,
                             byref(src_c_ubyte),
                             len(src),
                             dst,
                             use_shared_key)
         if ret < 0:
            raise AssertionError('bad return code %d' % ret)

      if src_is_file and not dst_is_file:
         ret = self._zkLockDataF2B(self._zk_ctx,
                             src,
                             byref(dst_data),
                             byref(dst_data_sz),
                             use_shared_key)
         if ret < 0:
            raise AssertionError('bad return code %d' % ret)
         dc = (c_ubyte * dst_data_sz.value).from_address(dst_data.value)
         data_array = bytearray(dc)
         return data_array

      if not src_is_file and not dst_is_file:
         ret = self._zkLockDataB2B(self._zk_ctx,
                             byref(src_c_ubyte),
                             len(src),
                             byref(dst_data),
                             byref(dst_data_sz),
                             use_shared_key)
         if ret < 0:
            raise AssertionError('bad return code %d' % ret)
         dc = (c_ubyte * dst_data_sz.value).from_address(dst_data.value)
         data_array = bytearray(dc)
         return data_array
   ###@}

   ## @name Unlock Data
   ###@{

   ## @brief Unlock source (ciphertext) data.
   #  @details This method verifies a locked object signature and
   #           decrypts the associated ciphertext data.
   #
   #    The zymkey has two keys that can be used for locking/unlocking
   #    operations, designated as shared and one-way.
   #      1. The one-way key is meant to lock up data only on the
   #         local host computer. Data encrypted using this key cannot
   #         be exported and deciphered anywhere else.
   #      2. The shared key is meant for publishing data to other
   #         sources that have the capability to generate the shared
   #         key, such as the Zymbit cloud server.
   #
   #  @param src The source (ciphertext) data. If typed as a
   #    basestring, it is assumed to be an absolute file name path
   #    where the source file is located, otherwise it is assumed to
   #    contain binary data.
   #  @param dst The destination (plaintext) data. If specified as a
   #    basestring, it is assumed to be an absolute file name path
   #    where the destination data is meant to be deposited. Otherwise,
   #    the locked data result is returned from the method call as a
   #    bytearray. The default is 'None', which means that the data
   #    will be returned to the caller as a bytearray.
   #  @param encryption_key Specifies which key will be
   #    used to unlock the source data. A value of 'zymkey' (default)
   #    specifies that the Zymkey will use the one-way key. A value of
   #    'cloud' specifies that the shared key is used. Specify 'cloud'
   #    for publishing data to another source that has the shared key
   #    (e.g. Zymbit cloud) and 'zymkey' when the data is meant to
   #    reside exclusively withing the host computer.
   #  @param raise_exception Specifies if an exception should be raised
   #    if the locked object signature fails.
   def unlock(self, src, dst=None, encryption_key=ZYMKEY_ENCRYPTION_KEY, raise_exception=True):
      # Determine if source and destination are strings. If so, they must be
      # filenames
      src_is_file = is_string(src)
      dst_is_file = is_string(dst)

      assert encryption_key in ENCRYPTION_KEYS
      use_shared_key = encryption_key == CLOUD_ENCRYPTION_KEY

      # Prepare src if it is not specifying a filename
      if not src_is_file:
         src_sz = len(src)
         src_c_ubyte = (c_ubyte * src_sz)(*src)
      else:
         src = src.encode('utf-8')
      # Prepare dst if it is not specifying a filename
      if not dst_is_file:
         dst_data = c_void_p()
         dst_data_sz = c_int()
      else:
         dst = dst.encode('utf-8')
      if src_is_file and dst_is_file:
         ret = self._zkUnlockDataF2F(self._zk_ctx,
                              src,
                              dst,
                              use_shared_key)
         if ret < 0:
            raise AssertionError('bad return code %d' % ret)

      if not src_is_file and dst_is_file:
         ret = self._zkUnlockDataB2F(self._zk_ctx,
                              byref(src_c_ubyte),
                              len(src),
                              dst,
                              use_shared_key)
         if ret < 0:
            raise AssertionError('bad return code %d' % ret)

      if src_is_file and not dst_is_file:
         ret = self._zkUnlockDataF2B(self._zk_ctx,
                              src,
                              byref(dst_data),
                              byref(dst_data_sz),
                              use_shared_key)
         if ret < 0:
            raise AssertionError('bad return code %d' % ret)
         dc = (c_ubyte * dst_data_sz.value).from_address(dst_data.value)
         data_array = bytearray(dc)
         return data_array

      if not src_is_file and not dst_is_file:
         ret = self._zkUnlockDataB2B(self._zk_ctx,
                              byref(src_c_ubyte),
                              len(src),
                              byref(dst_data),
                              byref(dst_data_sz),
                              use_shared_key)
         if ret < 0:
            raise AssertionError('bad return code %d' % ret)
         if ret == 0:
            if raise_exception:
               raise VerificationError()
            return None
         if ret == 1:
            dc = (c_ubyte * dst_data_sz.value).from_address(dst_data.value)
            data_array = bytearray(dc)
            return data_array
   ###@}

   ## @name ECDSA
   ###@{

   ## @brief Generate a signature using the Zymkey's ECDSA private key.
   #  @param src This parameter contains the digest of the data that
   #    will be used to generate the signature.
   #  @param slot This parameter specifies the key slot used for signing.
   #  @returns a byte array of the signature
   #  @todo Allow for overloading of source parameter in similar
   #    fashion to lock/unlockData.
   def sign(self, src, slot=0):
      sha256 = hashlib.sha256()
      sha256.update(src.encode('utf-8'))

      return self.sign_digest(sha256, slot=slot)

   ## @brief Generate a signature using the Zymkey's ECDSA private key.
   #  @param sha256 A hashlib.sha256 instance.
   #  @param slot This parameter specifies the key slot used for signing.
   #  @todo Allow for overloading of source parameter in similar
   #    fashion to lock/unlockData.
   def sign_digest(self, sha256, slot=0):
      digest_bytes = bytearray(sha256.digest())

      src_sz = len(digest_bytes)
      src_c_ubyte = (c_ubyte * src_sz)(*digest_bytes)
      dst_data = c_void_p()
      dst_data_sz = c_int()

      ret = self._zkGenECDSASigFromDigest(
         self._zk_ctx,
         src_c_ubyte,
         slot,
         byref(dst_data),
         byref(dst_data_sz)
      )
      if ret < 0:
         raise AssertionError('bad return code %d' % ret)
      dc = (c_ubyte * dst_data_sz.value).from_address(dst_data.value)
      data_array = bytearray(dc)
      return data_array

   ## @brief Verify the given buffer against the given signature.
   #    The public key is not specified in the parameter list to ensure
   #    that the public key that matches the Zymkey's ECDSA private key
   #    is used.
   #  @param src The buffer to verify
   #  @param sig This parameter contains the signature to verify.
   #  @param raise_exception By default, when verification fails a
   #    VerificationError will be raised, unless this is set to False
   #  @param pubkey_slot The key slot to use to verify the signature against. Defaults to the first key slot.
   #  @param foreign If false, the normal key store is referenced.
   #  Otherwise, the foreign public key store is referenced.
   #  @returns True for a good verification or False for a bad verification when raise_exception is False
   def verify(self, src, sig, raise_exception=True, pubkey_slot=0, foreign=False):
      sha256 = hashlib.sha256()
      sha256.update(src.encode('utf-8'))

      return self.verify_digest(sha256, sig, raise_exception=raise_exception, pubkey_slot=pubkey_slot, foreign=foreign)

   ## @brief Verify a signature using the Zymkey's ECDSA public key.
   #    The public key is not specified in the parameter list to ensure
   #    that the public key that matches the Zymkey's ECDSA private key
   #    is used.
   #  @param sha256 A hashlib.sha256 instance that
   #    will be used to generate the signature.
   #  @param sig This parameter contains the signature to verify.
   #  @param raise_exception By default, when verification fails a
   #    VerificationError will be raised, unless this is set to False
   #  @param pubkey_slot The key slot to use to verify the signature against. Defaults to the first key slot.
   #  @param foreign If false, the normal key store is referenced.
   #  Otherwise, the foreign public key store is referenced.
   #  @returns True for a good verification or False for a bad verification when raise_exception is False
   def verify_digest(self, sha256, sig, raise_exception=True, pubkey_slot=0, foreign=False):
        digest_bytes = bytearray(sha256.digest())

        src_sz = len(digest_bytes)
        sig_sz = len(sig)
        src_c_ubyte = (c_ubyte * src_sz)(*digest_bytes)
        sig_c_ubyte = (c_ubyte * sig_sz)(*sig)

        if not foreign:
            ret = self._zkVerifyECDSASigFromDigest(self._zk_ctx,
                                                   src_c_ubyte,
                                                   pubkey_slot,
                                                   sig_c_ubyte,
                                                   sig_sz)
        else:
            ret = self._zkVerifyECDSASigFromDigestWithForeignKeySlot(self._zk_ctx,
                                                                     src_c_ubyte,
                                                                     pubkey_slot,
                                                                     sig_c_ubyte,
                                                                     sig_sz)

        if ret == 0:
            if raise_exception:
                raise VerificationError()
            return False
        if ret == 1:
            return True
        else:
            raise AssertionError('bad return code %d' % ret)
   ###@}

   ## @name ECDH and KDF
   ###@{

   ## @brief Derive a key or a pre-master secret from an ECDH operation (model >= HSM6).
   #  @param local_slot This parameter specifies the local key slot to use.
   #  @param peer_pubkey
   #  @param kdf_func_type
   #  @param salt
   #  @param info
   #  @returns a byte array of the signature
   #  @todo Allow for overloading of source parameter in similar
   #    fashion to lock/unlockData.
   def ecdh(self, local_slot, peer_pubkey, kdf_func_type="none", salt=[], info=[], num_iterations=1, peer_pubkey_slot_is_foreign=True, derived_key_size=32):
      derived_key = c_void_p()
      salt_sz = len(salt)
      salt_c_ubyte = (c_ubyte * salt_sz)(*salt)
      info_sz = len(info)
      info_c_ubyte = (c_ubyte * info_sz)(*info)
      # Get the kdf_func_type
      kdf_func = kdfFuncTypes[kdf_func_type]
      # Get the type of the peer public key. If the type is 'int', peer_pubkey
      # refers to a slot internal to the zymkey. Otherwise, a list with the
      # contents of the public key is expected.
      if type(peer_pubkey) == 'int' or type(peer_pubkey) is int:
         peer_pubkey = c_int(peer_pubkey)
         peer_pubkey_slot_is_foreign = c_bool(peer_pubkey_slot_is_foreign)
         if kdf_func_type == "none":
            self._zkDoRawECDHWithIntPeerPubkey(self._zk_ctx, local_slot, peer_pubkey, peer_pubkey_slot_is_foreign, byref(derived_key))
            dst_data_sz = c_int(32)
         else:
            self._zkDoECDHAndKDFWithInterPeerPubkey(self._zk_ctx,
                                                    kdf_func-1,
                                                    local_slot,
                                                    peer_pubkey,
                                                    peer_pubkey_slot_is_foreign,
                                                    salt_c_ubyte,
                                                    salt_sz,
                                                    info_c_ubyte,
                                                    info_sz,
                                                    num_iterations,
                                                    derived_key_size,
                                                    byref(derived_key))
      else:
         peer_pubkey_sz = len(peer_pubkey)
         peer_pubkey_c_ubyte = (c_ubyte * peer_pubkey_sz)(*peer_pubkey)
         if kdf_func_type == "none":
            self._zkDoRawECDH(self._zk_ctx, local_slot, peer_pubkey_c_ubyte, peer_pubkey_sz, byref(derived_key))
            dst_data_sz = c_int(32)
         else:
            self._zkDoECDHAndKDF(self._zk_ctx,
                                 kdf_func-1,
                                 local_slot,
                                 peer_pubkey_c_ubyte,
                                 peer_pubkey_sz,
                                 salt_c_ubyte,
                                 salt_sz,
                                 info_c_ubyte,
                                 info_sz,
                                 num_iterations,
                                 derived_key_size,
                                 byref(derived_key))
      dc = (c_ubyte * derived_key_size).from_address(derived_key.value)
      data_array = bytearray(dc)
      return data_array
   ###@}

   ## @name Key Management
   ###@{

   ## @brief [DEPRECATED] Use create_public_key_file. Create a file with the PEM-formatted ECDSA public key.
   #  @details This method is useful for generating a Certificate
   #           Signing Request.
   #  @param filename The absolute file path where the public key will
   #    be stored in PEM format.
   #  @param slot This parameter specifies the key slot for the public
   #              key.
   def create_ecdsa_public_key_file(self, filename, slot=0):
      ret = self._zkSaveECDSAPubKey2File(self._zk_ctx, filename.encode('utf-8'), slot)
      if ret < 0:
         raise AssertionError('bad return code %d' % ret)

   ## @brief Create a file with the PEM-formatted public key.
   #  @details This method is useful for generating a Certificate
   #           Signing Request.
   #  @param filename The absolute file path where the public key will
   #    be stored in PEM format.
   #  @param slot This parameter specifies the key slot for the public
   #              key. Zymkey and HSM4 have slots 0, 1, and 2.
   #  @param slot_is_foreign
   #        If true, designates the pubkey slot to come from the foreign
   #        keystore (model >= HSM6).
   def create_public_key_file(self, filename, slot=0, foreign=False):
      ret = self._zkExportPubKey2File(self._zk_ctx, filename.encode('utf-8'), slot, foreign)
      if ret < 0:
         raise AssertionError('bad return code %d' % ret)

   ## @brief [DEPRECATED] Use get_public_key. Retrieves the ECDSA public key as a binary bytearray.
   #  @details This method is used to retrieve the public key in binary
   #           form.
   #  @param slot This parameter specifies the key slot for the public
   #              key.
   def get_ecdsa_public_key(self, slot=0):
      dst_data = c_void_p()
      dst_data_sz = c_int()

      ret = self._zkGetECDSAPubKey(self._zk_ctx, byref(dst_data), byref(dst_data_sz), slot)
      if ret < 0:
         raise AssertionError('bad return code %d' % ret)
      dc = (c_ubyte * dst_data_sz.value).from_address(dst_data.value)
      data_array = bytearray(dc)
      return data_array

   ## @brief Retrieves a public key as a binary bytearray.
   #  @details This method is used to retrieve the public key in binary
   #           form.
   #  @param slot This parameter specifies the key slot for the public
   #              key. Zymkey and HSM4 have slots 0, 1, and 2.
   #  @return Bytearray of the public key
   def get_public_key(self, slot=0, foreign=False):
      dst_data = c_void_p()
      dst_data_sz = c_int()

      ret = self._zkExportPubKey(self._zk_ctx, byref(dst_data), byref(dst_data_sz), slot, foreign)
      if ret < 0:
         raise AssertionError('bad return code %d' % ret)
      dc = (c_ubyte * dst_data_sz.value).from_address(dst_data.value)
      data_array = bytearray(dc)
      return data_array

   ## @brief Get a list of the allocated slots in the key store (model >= HSM6).
   #  @details This method gets a list of the allocated slots in the key
   #           store.
   #  @param foreign If True, the allocation list of the foreign key
   #                 store is returned
   #  @return the allocation list and the maximum number of keys
   def get_slot_alloc_list(self, foreign=False):
      alloc_key_slot_list = c_void_p()
      alloc_key_slot_list_sz = c_int()
      max_num_keys = c_int()

      ret = self._zkGetAllocSlotsList(self._zk_ctx, foreign, byref(max_num_keys), byref(alloc_key_slot_list), byref(alloc_key_slot_list_sz))
      if ret < 0:
         raise AssertionError('bad return code %d' % ret)
      dc = (c_int * alloc_key_slot_list_sz.value).from_address(alloc_key_slot_list.value)
      alloc_keys = list(dc)
      return alloc_keys, max_num_keys.value

   ## @brief Stores a foreign public key on the Zymkey foreign keyring (model >= HSM6).
   #  @details This method stores a foreign public key onto the Zymkey foreign
   #           public keyring.
   #  @param key_type This parameter indicates the EC curve type that should be
   #                  associated with the public key
   #  @param pubkey The public key binary data
   #  @return the slot allocated to the key or less than one for failure.
   def store_foreign_public_key(self, key_type, pubkey):
      pubkey_sz = len(pubkey)
      pubkey_c_ubyte = (c_ubyte * pubkey_sz)(*pubkey)

      kt = keyTypes[key_type]
      ret = self._zkStoreForeignPubKey(self._zk_ctx, kt, pubkey_c_ubyte, pubkey_sz)
      if ret < 0:
         raise AssertionError('bad return code %d' % ret)
      return ret

   ## @brief Disables exporting of a public key at a given slot (model >= HSM6).
   #  @details This method permanently disables exporting a public key from a
   #           given slot.
   #  @param slot This parameter specifies the key slot for the public
   #              key.
   #  @param foreign If true, the slot refers to the foreign public keyring.
   def disable_public_key_export(self, slot=0, foreign=False):
      ret = self._zkDisablePubKeyExport(self._zk_ctx, slot, foreign)
      if ret < 0:
         raise AssertionError('bad return code %d' % ret)

   ## @brief Generates a new key pair (model >= HSM6).
   #  @details This method generates a new key pair of the specified type.
   #  @param key_type This parameter indicates the EC curve type that should be
   #                  associated with the new key pair.
   #  @return the slot allocated to the key or less than one for failure.
   def gen_key_pair(self, key_type):
      kt = keyTypes[key_type]
      ret = self._zkGenKeyPair(self._zk_ctx, kt)
      if ret < 0:
         raise AssertionError('bad return code %d' % ret)
      return ret

   ## @brief Generates a new ephemeral key pair (model >= HSM6).
   #  @details This method generates a new ephemeral key pair of the specified
   #           type, overwriting the previous ephemeral key pair.
   #  @param key_type This parameter indicates the EC curve type that should be
   #                  associated with the new key pair.
   def gen_ephemeral_key_pair(self, key_type):
      kt = keyTypes[key_type]
      ret = self._zkGenEphemeralKeyPair(self._zk_ctx, kt)
      if ret < 0:
         raise AssertionError('bad return code %d' % ret)

   ## @brief Remove a key at the designated slot (model >= HSM6).
   #  @details This method removes a key at the designated slot in either the
   #           standard key store or the foreign public keyring.
   #  @param slot This parameter specifies the key slot for the key.
   #  @param foreign If true, a public key in the foreign keyring will be
   #                 deleted.
   def remove_key(self, slot, foreign=False):
      ret = self._zkRemoveKey(self._zk_ctx, slot, foreign)
      if ret < 0:
         raise AssertionError('bad return code %d' % ret)

   ## @brief Invalidate the ephemeral key (model >= HSM6).
   #  @details This method invalidates the ephemeral key, effectively removing
   #           it from service until a new key is generated.
   def invalidate_ephemeral_key(self, slot, foreign=False):
      ret = self._zkInvalidateEphemeralKey(self._zk_ctx)
      if ret < 0:
         raise AssertionError('bad return code %d' % ret)
      return ret
   ###@}

   ## @name Digital Wallet (BIP 32/39/44)
   ###@{

   ## @brief Generates a new master seed for creating a new BIP32 wallet (model >= HSM6).
   #  @details This method generates a new master seed for creating a new BIP32
   #           wallet.
   #  @param key_type This parameter indicates the EC curve type that should be
   #                  associated with the new key pair.
   #  @param master_gen_key The master generator key (bytearray) used in the
   #                        derivation of the child key.
   #  @param wallet_name The name of the wallet (string) that this master seed
   #                     is attached to.
   #  @param bip39 If true, generate the seed per BIP39 and return the mnemonic
   #               string.
   #  @return a tuple with the slot and the BIP39 mnemonic if specified
   def gen_wallet_master_seed(self, key_type, master_gen_key, wallet_name, bip39=False):
      master_gen_key_sz = len(master_gen_key)
      master_gen_key_c_ubyte = (c_ubyte * master_gen_key_sz)(*master_gen_key)
      bip39_mnemonic = c_void_p()
      if bip39:
         mnemonic_ptr = byref(bip39_mnemonic)
      else:
         mnemonic_ptr = POINTER(c_void_p)()

      kt = keyTypes[key_type]
      ret = self._zkGenWalletMasterSeed(self._zk_ctx,
                                        kt,
                                        wallet_name.encode('utf-8'),
                                        master_gen_key_c_ubyte,
                                        master_gen_key_sz,
                                        mnemonic_ptr)
      if ret < 0:
         raise AssertionError('bad return code %d' % ret)
      if bip39:
          mnemonic = cast(bip39_mnemonic, c_char_p)
          return ret, mnemonic.value.decode('utf-8')
      else:
          return ret, None

   ## @brief Generates a child key based on a parent key that is in a wallet (model >= HSM6).
   #  @details This method generates a child key based on a parent key that is
   #           in a wallet.
   #  @param parent_key_slot This parameter specifies the parent key slot. This
   #                         key must already be part of a wallet.
   #  @param index This parameter represents the index for the child key
   #               derivation which becomes part of the node address.
   #  @param hardened If true, the key is a hardened key.
   #  @return the allocated slot on success
   def gen_wallet_child_key(self, parent_key_slot, index, hardened):
      ret = self._zkGenWalletChildKey(self._zk_ctx, parent_key_slot, index, hardened)
      if ret < 0:
         raise AssertionError('bad return code %d' % ret)
      return ret

   ## @brief Restore a wallet's master seed based on a BIP39 mnemonic string (model >= HSM6).
   #  @details This method restores a wallet's master seed based on a BIP39
   #           mnemonic string and a master generator key. This method can be
   #           used in the process of wallet duplication.
   #  @param key_type This parameter indicates the EC curve type that should be
   #                  associated with the new key pair.
   #  @param master_gen_key The master generator key used in the derivation of
   #                        the child key.
   #  @param bip39_mnemonic The BIP39 mnemonic string.
   #  @return the allocated slot on success
   def restore_wallet_master_seed_from_bip39_mnemonic(self, key_type, master_gen_key, wallet_name, bip39_mnemonic):
      master_gen_key_sz = len(master_gen_key)
      master_gen_key_c_ubyte = (c_ubyte * master_gen_key_sz)(*master_gen_key)

      kt = keyTypes[key_type]
      ret = self._zkRestoreWalletMasterSeedFromMnemonic(self._zk_ctx,
                                                        kt,
                                                        wallet_name.encode('utf-8'),
                                                        master_gen_key_c_ubyte,
                                                        master_gen_key_sz,
                                                        bip39_mnemonic.encode('utf-8'))
      if ret < 0:
         raise AssertionError('bad return code %d' % ret)
      return ret

   ## @brief Get a wallet node address from a key slot (model >= HSM6)
   #  @details This method gets a wallet entry's node address from its key slot
   #           assignment. The wallet name and master seed slot are also
   #          returned.
   #  @param slot The key slot assignment.
   #  @return the node address, wallet name and master seed key slot.
   def get_wallet_node_addr(self, slot):
       node_addr = c_void_p()
       wallet_name = c_void_p()
       master_seed_slot = c_int()
       ret = self._zkGetWalletNodeAddrFromKeySlot(self._zk_ctx, slot, byref(node_addr), byref(wallet_name), byref(master_seed_slot))
       if ret < 0:
           raise AssertionError('bad return code %d' % ret)
       na = cast(node_addr, c_char_p)
       wn = cast(wallet_name, c_char_p)
       return na.value.decode('utf-8'), wn.value.decode('utf-8'), master_seed_slot.value

   ## @brief Look up a wallet key slot number from a node address (model >= HSM6)
   #  @details This method gets a wallet key slot number from its node address
   #           and wallet name or master seed key slot. Either the wallet name
   #           or the master seed slot must be present.
   #  @param node_addr The desired node address to look up
   #  @param wallet_name The name of the wallet that the node address belongs
   #                     to. Either this parameter or master_seed_slot must be
   #                     specified or this function will fail.
   #  @param master_seed_slot The master seed slot that the node address belongs
   #                          to. Either this parameter or wallet_name must be
   #                          specified or this function will fail.
   #  @return the key slot.
   def get_wallet_key_slot(self, node_addr, wallet_name=None, master_seed_slot=None):
       if wallet_name:
           wallet_name = wallet_name.encode('utf-8')
           master_seed_slot = 0
       key_slot = c_int()
       ret = self._zkGetWalletKeySlotFromNodeAddr(self._zk_ctx, node_addr.encode('utf-8'), wallet_name, master_seed_slot, byref(key_slot))
       if ret < 0:
           raise AssertionError('bad return code %d' % ret)
       return key_slot.value
   ###@}

   ## @name Adminstration
   ###@{

   ## @brief Sets the i2c address of the Zymkey (i2c versions only)
   #  @details This method should be called if the i2c address of the
   #    Zymkey is shared with another i2c device on the same i2c bus.
   #    The default i2c address for Zymkey units is 0x30. Currently,
   #    the address may be set in the ranges of 0x30 - 0x37 and
   #    0x60 - 0x67.
   #
   #    After successful completion of this command, the Zymkey will
   #    reset itself.
   #  @param address The i2c address that the Zymkey will set itself
   #    to.
   def set_i2c_address(self, address):
      addr_c_int = c_int(address)
      ret = self._zkSetI2CAddr(self._zk_ctx, addr_c_int)
      if ret < 0:
         raise AssertionError('bad return code %d' % ret)
   ###@}

   ## @name Accelerometer
   ###@{

   ## @brief Sets the sensitivity of tap operations.
   #  @details This method permits setting the sensitivity of the tap
   #           detection feature. Each axis may be individually
   #           configured or all at once.
   # @param axis The axis to configure. Valid values include:
   #   1. 'all': Configure all axes with the specified sensitivity
   #      value.
   #   2. 'x' or 'X': Configure only the x-axis
   #   3. 'y' or 'Y': Configure only the y-axis
   #   4. 'z' or 'Z': Configure only the z-axis
   # @param pct The sensitivity expressed as percentage.
   #   1. 0% = Shut down: Tap detection should not occur along the
   #      axis.
   #   2. 100% = Maximum sensitivity.
   def set_tap_sensitivity(self, axis='all', pct=50.0):
      axis = axis.lower()
      axis_c_int = c_int()
      if axis == 'x':
         axis_c_int = 0
      elif axis == 'y':
         axis_c_int = 1
      elif axis == 'z':
         axis_c_int = 2
      elif axis == 'all':
         axis_c_int = 3
      else:
         raise AssertionError('invalid input value ' + axis)
      ret = self._zkSetTapSensitivity(self._zk_ctx, axis_c_int, pct)
      if ret < 0:
         raise AssertionError('bad return code %d' % ret)

   ## @brief Wait for tap event
   #  @brief Wait for a tap event to be detected
   #  @details This function is called in order to wait for a tap event to occur.
   #           This function blocks the calling thread unless called with a
   #           timeout of zero.
   #  @param timeout_ms
   #         (input) The maximum amount of time in milliseconds to wait for a tap
   #         event to arrive.
   def wait_for_tap(self, timeout_ms=-1):
      ret = self._zkWaitForTap(self._zk_ctx, timeout_ms)
      if ret == -errno.ETIMEDOUT:
         raise ZymkeyTimeoutError('wait timed out')
      if ret < 0:
         raise AssertionError('bad return code %d' % ret)

   class ZymkeyAccelAxisData(object):
      def __init__(self, g_force, tap_dir):
         self.g_force = g_force
         self.tap_dir = tap_dir

   ## @brief Get current accelerometer data and tap info.
   #  @details This function gets the most recent accelerometer data in units of g
   #           forces plus the tap direction per axis.
   #  @param x
   #         (output) An array of accelerometer readings in units of g-force.
   #                  array index 0 = x axis
   #                              1 = y axis
   #                              2 = z axis
   #         tap_dir
   #         (output) The directional information for the last tap event. A value
   #                  of -1 indicates that the tap event was detected in a
   #                  negative direction for the axis, +1 for a positive direction
   #                  and 0 for stationary.
   def get_accelerometer_data(self):
      class _zkAccelAxisDataType(Structure):
         _fields_ = [("g",            c_double),
                  ("tapDirection", c_int)]

      x = _zkAccelAxisDataType()
      y = _zkAccelAxisDataType()
      z = _zkAccelAxisDataType()
      ret = self._zkGetAccelerometerData(self._zk_ctx, byref(x), byref(y), byref(z))
      if ret < 0:
         raise AssertionError('bad return code %d' % ret)
      xret = self.ZymkeyAccelAxisData(x.g, x.tapDirection)
      yret = self.ZymkeyAccelAxisData(y.g, y.tapDirection)
      zret = self.ZymkeyAccelAxisData(z.g, z.tapDirection)
      return xret, yret, zret
   ###@}

   ## @name Time
   ###@{

   ## @brief Get current GMT time
   #  @details This function is called to get the time directly from a
   #           Zymkey's Real Time Clock (RTC)
   # @param precise If true, this API returns the time after the next second
   #        falls. This means that the caller could be blocked up to one second.
   #        If False, the API returns immediately with the current time reading.
   # @returns The time in seconds from the epoch (Jan. 1, 1970)
   def get_time(self, precise=False):
      epoch_sec = c_int()
      ret = self._zkGetTime(self._zk_ctx, byref(epoch_sec), precise)
      if ret < 0:
         raise AssertionError('bad return code %d' % ret)
      return epoch_sec.value
   ###@}

   ## @name Binding Management
   ###@{

   ## @brief Set soft binding lock.
   # @details This function locks the binding for a specific HSM. This API is
   #          only valid for HSM series products.
   # @exceptions AssertionError
   def lock_binding(self):
      ret = self._zkLockBinding(self._zk_ctx)
      if ret < 0:
         raise AssertionError('bad return code %d' % ret)

   ## @brief Get current binding info
   # @details This function gets the current binding lock state as well as the
   #          current binding state. This API is only valid for devices in the HSM
   #          family.
   # @param binding_is_locked
   #        (output) Binary value which expresses the current binding lock state.
   #        is_bound
   #        (output) Binary value which expresses the current bind state.
   # @returns locked, is_bound
   # @exceptions AssertionError
   def get_current_binding_info(self):
      locked = c_bool()
      is_bound = c_bool()
      ret = self._zkGetCurrentBindingInfo(self._zk_ctx, byref(locked), byref(is_bound))
      if ret < 0:
         raise AssertionError('bad return code %d' % ret)
      return locked.value, is_bound.value
   ###@}

   ## @name Perimeter Breach
   ###@{

   ## @brief Set perimeter breach action
   #  @details This function specifies the action to take when a perimeter breach
   #           event occurs. The possible actions are any combination of:
   #               - Notify host
   #               - Zymkey self-destruct
   #  @param channel
   #         (input) The channel (0 or 1) that the action flags will be applied to
   #  @param action_notify
   #         (input) Set a perimeter breach to notify. (default = True)
   #  @param action_self_destruct
   #         (input) Set a perimeter breach to self destruct. (default = False)
   def set_perimeter_event_actions(self, channel, action_notify=True, action_self_destruct=False):
      actions = 0
      if action_notify:
         actions |= 1
      if action_self_destruct:
         actions |= 2
      ret = self._zkSetPerimeterEventAction(self._zk_ctx, channel, actions)
      if ret < 0:
         raise AssertionError('bad return code %d' % ret)

   ## @brief Set the digital perimeter detect low power period (model >= HSM6).
   #  @details This function sets the digital perimeter detect low power period (microseconds).
   #  @param lp_period The perimeter detect low power period in microseconds.
   def set_digital_perimeter_lp_period(self, lp_period):
      ret = self._zkSetDigitalPerimeterDetectLPPeriod(self._zk_ctx, lp_period)
      if ret < 0:
         raise AssertionError('bad return code %d' % ret)

   ## @brief Set the low power max number of bits (model >= HSM6).
   #  @details This function sets the digital perimeter detect low power max number of bits
   #  @param max_num_bits The perimeter detect low power max number of bits
   def set_digital_perimeter_lp_max_bits(self, max_num_bits):
      ret = self._zkSetDigitalPerimeterDetectLPMaxBits(self._zk_ctx, max_num_bits)
      if ret < 0:
         raise AssertionError('bad return code %d' % ret)

   ## @brief Set the digital perimeter detect delays (model >= HSM6).
   #  @details This function sets the digital perimeter detect delay values.
   #  @param min_delay_ns The minimum delay in nanoseconds
   #  @param max_delay_ns The maximum delay in nanoseconds
   def set_digital_perimeter_delays(self, min_delay_ns, max_delay_ns):
      ret = self._zkSetDigitalPerimeterDetectDelays(self._zk_ctx, min_delay_ns, max_delay_ns)
      if ret < 0:
         raise AssertionError('bad return code %d' % ret)

   ## @brief Wait for a perimeter breach event to be detected
   #  @details This function is called in order to wait for a perimeter breach
   #           event to occur. This function blocks the calling thread unless
   #           called with a timeout of zero.
   #  @param timeout_ms
   #         (input) The maximum amount of time in milliseconds to wait for a perimeter breach
   #         event to arrive.
   def wait_for_perimeter_event(self, timeout_ms=-1):
      ret = self._zkWaitForPerimeterEvent(self._zk_ctx, timeout_ms)
      if ret == -errno.ETIMEDOUT:
         raise ZymkeyTimeoutError('wait timed out')
      if ret < 0:
         raise AssertionError('bad return code %d' % ret)

   ##  @brief Get current perimeter detect info.
   #  @details This function gets the timestamp of the first perimeter detect
   #           event for the given channel. The index corresponds to the channel specified in set_perimeter_event_actions.
   #  @returns The array of timestamps for each channel for the first detected
   #           event in epoch seconds
   def get_perimeter_detect_info(self):
      pdata = c_void_p()
      pdata_sz = c_int()

      ret = self._zkGetPerimeterDetectInfo(self._zk_ctx, byref(pdata), byref(pdata_sz))
      if ret < 0:
         raise AssertionError('bad return code %d' % ret)
      dc = (c_uint32 * pdata_sz.value).from_address(pdata.value)

      timestamps_sec = []

      for i in range(pdata_sz.value):
         timestamps_sec.append(dc[i])
      return timestamps_sec

   ## @brief Clear perimeter detect info.
   #  @details This function clears all perimeter detect info and rearms all
   #           perimeter detect channels
   def clear_perimeter_detect_info(self):
      ret = self._zkClearPerimeterDetectEvents(self._zk_ctx)
      if ret < 0:
         raise AssertionError('bad return code %d' % ret)
   ###@}

   ## @name Module Info
   ###@{

   ## @brief Get current CPU temperature (model >= HSM6).
   #  @details This function gets the current HSM CPU temperature.
   #  @returns The CPU temperature in celsius as a float
   def get_cpu_temp(self):
      temp = c_float()
      ret = self._zkGetCPUTemp(self._zk_ctx, byref(temp))
      if ret < 0:
         raise AssertionError('bad return code %d' % ret)
      return temp.value

   ## @brief Get RTC drift (model >= HSM6).
   #  @details This function gets the current RTC drift.
   #  @returns The RTC drift as a float
   def get_rtc_drift(self):
      drift = c_float()
      ret = self._zkGetRTCDrift(self._zk_ctx, byref(drift))
      if ret < 0:
         raise AssertionError('bad return code %d' % ret)
      return drift.value

   ## @brief Get current battery voltage (model >= HSM6).
   #  @details This function gets the current battery voltage.
   #  @returns The battery voltage as a float
   def get_batt_volt(self):
      volt = c_float()
      ret = self._zkGetBatteryVoltage(self._zk_ctx, byref(volt))
      if ret < 0:
         raise AssertionError('bad return code %d' % ret)
      return volt.value

   ###@}

   ## @name Model Information
   ###@{
   ## @brief Get Zymkey model number
   #  @details This function gets the Zymkey model number.
   #  @returns The model number as a string.
   def get_model_number(self):
      model = c_void_p()
      ret = self._zkGetModelNumberString(self._zk_ctx, byref(model))
      if ret < 0:
         raise AssertionError('bad return code %d' % ret)
      model_str = cast(model, c_char_p)
      return model_str.value.decode('utf-8')

   ## @brief Get Zymkey firmware version
   #  @details This function gets the Zymkey firmware version.
   #  @returns The firmware version as a string.
   def get_firmware_version(self):
      fw = c_void_p()
      ret = self._zkGetFirmwareVersionString(self._zk_ctx, byref(fw))
      if ret < 0:
         raise AssertionError('bad return code %d' % ret)
      fw_str = cast(fw, c_char_p)
      return fw_str.value.decode('utf-8')

   ## @brief Get Zymkey serial number
   #  @details This function gets the Zymkey serial number.
   #  @returns The serial number as a string.
   def get_serial_number(self):
      sn = c_void_p()
      ret = self._zkGetSerialNumberString(self._zk_ctx, byref(sn))
      if ret < 0:
         raise AssertionError('bad return code %d' % ret)
      sn_str = cast(sn, c_char_p)
      return sn_str.value.decode('utf-8')
   ###@}



   # Interfaces to the C library
   _zkOpen = zkalib.zkOpen
   _zkOpen.restype = c_int
   _zkOpen.argtypes = [POINTER(c_void_p)]

   _zkClose = zkalib.zkClose
   _zkClose.restype = c_int
   _zkClose.argtypes = [c_void_p]

   _zkLEDOn = zkalib.zkLEDOn
   _zkLEDOn.restype = c_int
   _zkLEDOn.argtypes = [c_void_p]

   _zkLEDOff = zkalib.zkLEDOff
   _zkLEDOff.restype = c_int
   _zkLEDOff.argtypes = [c_void_p]

   _zkLEDFlash = zkalib.zkLEDFlash
   _zkLEDFlash.restype = c_int
   _zkLEDFlash.argtypes = [c_void_p, c_ulong, c_ulong, c_ulong]

   _zkGetRandBytes = zkalib.zkGetRandBytes
   _zkGetRandBytes.restype = c_int
   _zkGetRandBytes.argtypes = [c_void_p, POINTER(c_void_p), c_int]

   _zkCreateRandDataFile = zkalib.zkCreateRandDataFile
   _zkCreateRandDataFile.restype = c_int
   _zkCreateRandDataFile.argtypes = [c_void_p, c_char_p, c_int]

   _zkLockDataF2F = zkalib.zkLockDataF2F
   _zkLockDataF2F.restype = c_int
   _zkLockDataF2F.argtypes = [c_void_p, c_char_p, c_char_p, c_bool]

   _zkLockDataB2F = zkalib.zkLockDataB2F
   _zkLockDataB2F.restype = c_int
   _zkLockDataB2F.argtypes = [c_void_p, c_void_p, c_int, c_char_p, c_bool]

   _zkLockDataF2B = zkalib.zkLockDataF2B
   _zkLockDataF2B.restype = c_int
   _zkLockDataF2B.argtypes = [c_void_p, c_char_p, POINTER(c_void_p), POINTER(c_int), c_bool]

   _zkLockDataB2B = zkalib.zkLockDataB2B
   _zkLockDataB2B.restype = c_int
   _zkLockDataB2B.argtypes = [c_void_p, c_void_p, c_int, POINTER(c_void_p), POINTER(c_int), c_bool]

   _zkUnlockDataF2F = zkalib.zkUnlockDataF2F
   _zkUnlockDataF2F.restype = c_int
   _zkUnlockDataF2F.argtypes = [c_void_p, c_char_p, c_char_p, c_bool]

   _zkUnlockDataB2F = zkalib.zkUnlockDataB2F
   _zkUnlockDataB2F.restype = c_int
   _zkUnlockDataB2F.argtypes = [c_void_p, c_void_p, c_int, c_char_p, c_bool]

   _zkUnlockDataF2B = zkalib.zkUnlockDataF2B
   _zkUnlockDataF2B.restype = c_int
   _zkUnlockDataF2B.argtypes = [c_void_p, c_char_p, POINTER(c_void_p), POINTER(c_int), c_bool]

   _zkUnlockDataB2B = zkalib.zkUnlockDataB2B
   _zkUnlockDataB2B.restype = c_int
   _zkUnlockDataB2B.argtypes = [c_void_p, c_void_p, c_int, POINTER(c_void_p), POINTER(c_int), c_bool]

   _zkGenECDSASigFromDigest = zkalib.zkGenECDSASigFromDigest
   _zkGenECDSASigFromDigest.restype = c_int
   _zkGenECDSASigFromDigest.argtypes = [c_void_p, c_void_p, c_int, POINTER(c_void_p), POINTER(c_int)]

   _zkVerifyECDSASigFromDigest = zkalib.zkVerifyECDSASigFromDigest
   _zkVerifyECDSASigFromDigest.rettype = c_int
   _zkVerifyECDSASigFromDigest.argtypes = [c_void_p, c_void_p, c_int, c_void_p, c_int]

   try:
      _zkVerifyECDSASigFromDigestWithForeignKeySlot = zkalib.zkVerifyECDSASigFromDigestWithForeignKeySlot
      _zkVerifyECDSASigFromDigestWithForeignKeySlot.rettype = c_int
      _zkVerifyECDSASigFromDigestWithForeignKeySlot.argtypes = [c_void_p, c_void_p, c_int, c_void_p, c_int]

      _zkStoreForeignPubKey = zkalib.zkStoreForeignPubKey
      _zkStoreForeignPubKey.restype = c_int
      _zkStoreForeignPubKey.argtypes = [c_void_p, c_int, c_void_p, c_int]

      _zkDisablePubKeyExport = zkalib.zkDisablePubKeyExport
      _zkDisablePubKeyExport.restype = c_int
      _zkDisablePubKeyExport.argtypes = [c_void_p, c_int, c_bool]

      _zkGenKeyPair = zkalib.zkGenKeyPair
      _zkGenKeyPair.restype = c_int
      _zkGenKeyPair.argtypes = [c_void_p, c_int]

      _zkGenEphemeralKeyPair = zkalib.zkGenEphemeralKeyPair
      _zkGenEphemeralKeyPair.restype = c_int
      _zkGenEphemeralKeyPair.argtypes = [c_void_p, c_int]

      _zkRemoveKey = zkalib.zkRemoveKey
      _zkRemoveKey.restype = c_int
      _zkRemoveKey.argtypes = [c_void_p, c_int, c_bool]

      _zkInvalidateEphemeralKey = zkalib.zkInvalidateEphemeralKey
      _zkInvalidateEphemeralKey.restype = c_int
      _zkInvalidateEphemeralKey.argtypes = [c_void_p]

      _zkDoRawECDH = zkalib.zkDoRawECDH
      _zkDoRawECDH.restype = c_int
      _zkDoRawECDH.argtypes = [c_void_p, c_int, c_void_p, c_int, POINTER(c_void_p)]

      _zkDoRawECDHWithIntPeerPubkey = zkalib.zkDoRawECDHWithIntPeerPubkey
      _zkDoRawECDHWithIntPeerPubkey.restype = c_int
      _zkDoRawECDHWithIntPeerPubkey.argtypes = [c_void_p, c_int, c_int, c_bool, POINTER(c_void_p)]

      _zkDoECDHAndKDF = zkalib.zkDoECDHAndKDF
      _zkDoECDHAndKDF.restype = c_int
      _zkDoECDHAndKDF.argtypes = [c_void_p, c_int, c_int, c_void_p, c_int, c_void_p, c_int, c_void_p, c_int, c_int, c_int, POINTER(c_void_p)]

      _zkDoECDHAndKDFWithIntPeerPubkey = zkalib.zkDoECDHAndKDFWithIntPeerPubkey
      _zkDoECDHAndKDFWithIntPeerPubkey.restype = c_int
      _zkDoECDHAndKDFWithIntPeerPubkey.argtypes = [c_void_p, c_int, c_int, c_int, c_bool, c_void_p, c_int, c_void_p, c_int, c_int, c_int, POINTER(c_void_p)]

      _zkGenWalletMasterSeed = zkalib.zkGenWalletMasterSeed
      _zkGenWalletMasterSeed.restype = c_int
      _zkGenWalletMasterSeed.argtypes = [c_void_p, c_int, c_char_p, c_void_p, c_int, POINTER(c_void_p)]

      _zkRestoreWalletMasterSeedFromMnemonic = zkalib.zkRestoreWalletMasterSeedFromMnemonic
      _zkRestoreWalletMasterSeedFromMnemonic.restype = c_int
      _zkRestoreWalletMasterSeedFromMnemonic.argtypes = [c_void_p, c_int, c_char_p, c_void_p, c_int, c_char_p]

      _zkGenWalletChildKey = zkalib.zkGenWalletChildKey
      _zkGenWalletChildKey.restype = c_int
      _zkGenWalletChildKey.argtypes = [c_void_p, c_int, c_uint, c_bool]

      _zkGetWalletNodeAddrFromKeySlot = zkalib.zkGetWalletNodeAddrFromKeySlot
      _zkGetWalletNodeAddrFromKeySlot.restype = c_int
      _zkGetWalletNodeAddrFromKeySlot.argtypes = [c_void_p, c_int, POINTER(c_void_p), POINTER(c_void_p), POINTER(c_int)]

      _zkGetWalletKeySlotFromNodeAddr = zkalib.zkGetWalletKeySlotFromNodeAddr
      _zkGetWalletKeySlotFromNodeAddr.restype = c_int
      _zkGetWalletKeySlotFromNodeAddr.argtypes = [c_void_p, c_char_p, c_char_p, c_int, POINTER(c_int)]

      _zkGetAllocSlotsList = zkalib.zkGetAllocSlotsList
      _zkGetAllocSlotsList.restype = c_int
      _zkGetAllocSlotsList.argtypes = [c_void_p, c_bool, POINTER(c_int), POINTER(c_void_p), POINTER(c_int)]

      _zkExportPubKey2File = zkalib.zkExportPubKey2File
      _zkExportPubKey2File.restype = c_int
      _zkExportPubKey2File.argtypes = [c_void_p, c_char_p, c_int, c_bool]

      _zkExportPubKey = zkalib.zkExportPubKey
      _zkExportPubKey.restype = c_int
      _zkExportPubKey.argtypes = [c_void_p, POINTER(c_void_p), POINTER(c_int), c_int, c_bool]

      _zkLockBinding = zkalib.zkLockBinding
      _zkLockBinding.restype = c_int
      _zkLockBinding.argtypes = [c_void_p]

      _zkGetCurrentBindingInfo = zkalib.zkGetCurrentBindingInfo
      _zkGetCurrentBindingInfo.restype = c_int
      _zkGetCurrentBindingInfo.argtypes = [c_void_p, POINTER(c_bool), POINTER(c_bool)]

      _zkGetCPUTemp = zkalib.zkGetCPUTemp
      _zkGetCPUTemp.restype = c_int
      _zkGetCPUTemp.argtypes = [c_void_p, POINTER(c_float)]

      _zkGetRTCDrift = zkalib.zkGetRTCDrift
      _zkGetRTCDrift.restype = c_int
      _zkGetRTCDrift.argtypes = [c_void_p, POINTER(c_float)]

      _zkGetBatteryVoltage = zkalib.zkGetBatteryVoltage
      _zkGetBatteryVoltage.restype = c_int
      _zkGetBatteryVoltage.argtypes = [c_void_p, POINTER(c_float)]

      _zkSetDigitalPerimeterDetectLPPeriod = zkalib.zkSetDigitalPerimeterDetectLPPeriod
      _zkSetDigitalPerimeterDetectLPPeriod.restype = c_int
      _zkSetDigitalPerimeterDetectLPPeriod.argtypes = [c_void_p, c_int]

      _zkSetDigitalPerimeterDetectLPMaxBits = zkalib.zkSetDigitalPerimeterDetectLPMaxBits
      _zkSetDigitalPerimeterDetectLPMaxBits.restype = c_int
      _zkSetDigitalPerimeterDetectLPMaxBits.argtypes = [c_void_p, c_int]

      _zkSetDigitalPerimeterDetectDelays = zkalib.zkSetDigitalPerimeterDetectDelays
      _zkSetDigitalPerimeterDetectDelays.restype = c_int
      _zkSetDigitalPerimeterDetectDelays.argtypes = [c_void_p, c_int, c_int]

   except:
      pass

   _zkGetECDSAPubKey = zkalib.zkGetECDSAPubKey
   _zkGetECDSAPubKey.restype = c_int
   _zkGetECDSAPubKey.argtypes = [c_void_p, POINTER(c_void_p), POINTER(c_int), c_int]

   _zkSaveECDSAPubKey2File = zkalib.zkSaveECDSAPubKey2File
   _zkSaveECDSAPubKey2File.restype = c_int
   _zkSaveECDSAPubKey2File.argtypes = [c_void_p, c_char_p, c_int]

   _zkSetI2CAddr = zkalib.zkSetI2CAddr
   _zkSetI2CAddr.restype = c_int
   _zkSetI2CAddr.argtypes = [c_void_p, c_int]

   _zkSetTapSensitivity = zkalib.zkSetTapSensitivity
   _zkSetTapSensitivity.restype = c_int
   _zkSetTapSensitivity.argtypes = [c_void_p, c_int, c_float]

   _zkGetTime = zkalib.zkGetTime
   _zkGetTime.restype = c_int
   _zkGetTime.argtypes = [c_void_p, POINTER(c_int), c_bool]

   _zkWaitForTap = zkalib.zkWaitForTap
   _zkWaitForTap.restype = c_int
   _zkWaitForTap.argtypes = [c_void_p, c_int]

   _zkGetAccelerometerData = zkalib.zkGetAccelerometerData
   _zkGetAccelerometerData.restype = c_int
   _zkGetAccelerometerData.argtypes = [c_void_p, c_void_p, c_void_p, c_void_p]

   _zkWaitForPerimeterEvent = zkalib.zkWaitForPerimeterEvent
   _zkWaitForPerimeterEvent.restype = c_int
   _zkWaitForPerimeterEvent.argtypes = [c_void_p, c_int]

   _zkGetPerimeterDetectInfo = zkalib.zkGetPerimeterDetectInfo
   _zkGetPerimeterDetectInfo.restype = c_int
   _zkGetPerimeterDetectInfo.argtypes = [c_void_p, POINTER(c_void_p), POINTER(c_int)]

   _zkClearPerimeterDetectEvents = zkalib.zkClearPerimeterDetectEvents
   _zkClearPerimeterDetectEvents.restype = c_int
   _zkClearPerimeterDetectEvents.argtypes = [c_void_p]

   _zkSetPerimeterEventAction = zkalib.zkSetPerimeterEventAction
   _zkSetPerimeterEventAction.restype = c_int
   _zkSetPerimeterEventAction.argtypes = [c_void_p, c_int, c_int]

   _zkGetModelNumberString = zkalib.zkGetModelNumberString
   _zkGetModelNumberString.restype = c_int
   _zkGetModelNumberString.argtypes = [c_void_p, POINTER(c_void_p)]

   _zkGetFirmwareVersionString = zkalib.zkGetFirmwareVersionString
   _zkGetFirmwareVersionString.restype = c_int
   _zkGetFirmwareVersionString.argtypes = [c_void_p, POINTER(c_void_p)]

   _zkGetSerialNumberString = zkalib.zkGetSerialNumberString
   _zkGetSerialNumberString.restype = c_int
   _zkGetSerialNumberString.argtypes = [c_void_p, POINTER(c_void_p)]
